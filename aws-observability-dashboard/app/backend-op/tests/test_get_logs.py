"""GetLogs ハンドラ ユニットテスト（PBI-012）"""

import json
import os
import sys
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from handlers.get_logs import (
    lambda_handler,
    _parse_params,
    _build_query,
    _parse_log_entry,
    _process_results,
    _build_response,
    RANGE_CONFIG,
    VALID_LEVELS,
)


# ---------------------------------------------------------------------------
# ヘルパー
# ---------------------------------------------------------------------------

class FakeContext:
    aws_request_id = "test-request-id-002"


def _make_event(range_val=None, level=None, endpoint=None):
    params = {}
    if range_val is not None:
        params["range"] = range_val
    if level is not None:
        params["level"] = level
    if endpoint is not None:
        params["endpoint"] = endpoint
    return {
        "httpMethod": "GET",
        "resource": "/logs",
        "queryStringParameters": params if params else None,
    }


def _make_log_message(level="INFO", endpoint="GET /posts", message="テスト", **kwargs):
    data = {
        "timestamp": "2026-03-17T12:34:56Z",
        "level": level,
        "service": "demo-api",
        "endpoint": endpoint,
        "requestId": "abc-123",
        "message": message,
    }
    data.update(kwargs)
    return json.dumps(data)


def _make_cw_result(message, timestamp="2026-03-17 12:34:56.000"):
    return [
        {"field": "@timestamp", "value": timestamp},
        {"field": "@message", "value": message},
    ]


def _mock_logs_client(results=None, query_status="Complete", start_query_error=None):
    """テスト用の CloudWatch Logs クライアントモックを作成する。"""
    mock_client = MagicMock()

    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"logGroups": [{"logGroupName": "/aws/lambda/serverless-insight-demo-get_posts"}]}
    ]
    mock_client.get_paginator.return_value = mock_paginator

    if start_query_error:
        mock_client.start_query.side_effect = start_query_error
    else:
        mock_client.start_query.return_value = {"queryId": "test-query-id"}

    mock_client.get_query_results.return_value = {
        "status": query_status,
        "results": results if results is not None else [],
    }

    return mock_client


# ---------------------------------------------------------------------------
# テスト: パラメータ解析
# ---------------------------------------------------------------------------

class TestParseParams:
    def test_defaults(self):
        time_range, level, endpoint = _parse_params(_make_event())
        assert time_range == "1h"
        assert level is None
        assert endpoint is None

    def test_valid_range(self):
        for r in ("1h", "6h", "24h", "7d"):
            time_range, _, _ = _parse_params(_make_event(range_val=r))
            assert time_range == r

    def test_invalid_range_falls_back(self):
        time_range, _, _ = _parse_params(_make_event(range_val="99h"))
        assert time_range == "1h"

    def test_valid_level(self):
        for lv in ("INFO", "WARN", "ERROR"):
            _, level, _ = _parse_params(_make_event(level=lv))
            assert level == lv

    def test_invalid_level_ignored(self):
        _, level, _ = _parse_params(_make_event(level="DEBUG"))
        assert level is None

    def test_endpoint_filter(self):
        _, _, endpoint = _parse_params(_make_event(endpoint="GET /posts"))
        assert endpoint == "GET /posts"


# ---------------------------------------------------------------------------
# テスト: クエリ構築
# ---------------------------------------------------------------------------

class TestBuildQuery:
    def test_no_filter(self):
        query = _build_query()
        assert "filter" not in query
        assert "sort @timestamp desc" in query
        assert "limit 100" in query

    def test_level_filter(self):
        query = _build_query(level_filter="ERROR")
        assert '"level":"ERROR"' in query
        assert "filter" in query

    def test_no_level_no_filter(self):
        query = _build_query(level_filter=None)
        assert "filter" not in query


# ---------------------------------------------------------------------------
# テスト: ログエントリパース
# ---------------------------------------------------------------------------

class TestParseLogEntry:
    def test_valid_json(self):
        msg = _make_log_message(level="ERROR", statusCode=500, durationMs=100)
        entry = _parse_log_entry(msg)
        assert entry is not None
        assert entry["level"] == "ERROR"
        assert entry["statusCode"] == 500
        assert entry["durationMs"] == 100

    def test_invalid_json(self):
        entry = _parse_log_entry("not json")
        assert entry is None

    def test_empty_string(self):
        entry = _parse_log_entry("")
        assert entry is None

    def test_error_code_included(self):
        msg = _make_log_message(level="ERROR", errorCode="DDB_WRITE_FAILED")
        entry = _parse_log_entry(msg)
        assert entry["errorCode"] == "DDB_WRITE_FAILED"


# ---------------------------------------------------------------------------
# テスト: 結果処理
# ---------------------------------------------------------------------------

class TestProcessResults:
    def test_basic_processing(self):
        raw = [_make_cw_result(_make_log_message())]
        logs = _process_results(raw)
        assert len(logs) == 1
        assert logs[0]["level"] == "INFO"

    def test_endpoint_filter_match(self):
        raw = [
            _make_cw_result(_make_log_message(endpoint="GET /posts")),
            _make_cw_result(_make_log_message(endpoint="POST /posts")),
        ]
        logs = _process_results(raw, endpoint_filter="GET /posts")
        assert len(logs) == 1
        assert logs[0]["endpoint"] == "GET /posts"

    def test_endpoint_filter_no_match(self):
        raw = [_make_cw_result(_make_log_message(endpoint="GET /posts"))]
        logs = _process_results(raw, endpoint_filter="DELETE /posts")
        assert len(logs) == 0

    def test_non_json_skipped(self):
        raw = [
            _make_cw_result("START RequestId: abc-123"),
            _make_cw_result(_make_log_message()),
        ]
        logs = _process_results(raw)
        assert len(logs) == 1

    def test_fallback_timestamp(self):
        """構造化ログに timestamp がない場合 CW の @timestamp を使用する。"""
        msg = json.dumps({"level": "INFO", "message": "test"})
        raw = [_make_cw_result(msg, timestamp="2026-03-17 10:00:00.000")]
        logs = _process_results(raw)
        assert len(logs) == 1
        assert logs[0]["timestamp"] == "2026-03-17 10:00:00.000"


# ---------------------------------------------------------------------------
# テスト: レスポンス構築
# ---------------------------------------------------------------------------

class TestBuildResponse:
    def test_status_code_and_cors(self):
        resp = _build_response(200, {"ok": True})
        assert resp["statusCode"] == 200
        assert resp["headers"]["Access-Control-Allow-Origin"] == "*"
        body = json.loads(resp["body"])
        assert body["ok"] is True


# ---------------------------------------------------------------------------
# テスト: Lambda ハンドラ（CloudWatch モック）
# ---------------------------------------------------------------------------

class TestLambdaHandler:
    @patch("handlers.get_logs.boto3")
    def test_success_returns_logs(self, mock_boto3):
        """正常系: ログ一覧を取得できる"""
        mock_client = _mock_logs_client(
            results=[_make_cw_result(_make_log_message())]
        )
        mock_boto3.client.return_value = mock_client

        resp = lambda_handler(_make_event(), FakeContext())
        assert resp["statusCode"] == 200
        body = json.loads(resp["body"])
        assert body["count"] == 1
        assert len(body["logs"]) == 1
        assert body["timeRange"] == "1h"

    @patch("handlers.get_logs.boto3")
    def test_level_filter(self, mock_boto3):
        """レベルフィルタ: ERROR のみ取得"""
        mock_client = _mock_logs_client(
            results=[
                _make_cw_result(_make_log_message(level="ERROR", message="エラー発生")),
            ]
        )
        mock_boto3.client.return_value = mock_client

        resp = lambda_handler(_make_event(level="ERROR"), FakeContext())
        assert resp["statusCode"] == 200
        body = json.loads(resp["body"])
        assert body["count"] == 1
        assert body["logs"][0]["level"] == "ERROR"

    @patch("handlers.get_logs.boto3")
    def test_endpoint_filter(self, mock_boto3):
        """エンドポイントフィルタ: 特定エンドポイントのみ取得"""
        mock_client = _mock_logs_client(
            results=[
                _make_cw_result(_make_log_message(endpoint="GET /posts")),
                _make_cw_result(_make_log_message(endpoint="POST /posts")),
            ]
        )
        mock_boto3.client.return_value = mock_client

        resp = lambda_handler(_make_event(endpoint="GET /posts"), FakeContext())
        assert resp["statusCode"] == 200
        body = json.loads(resp["body"])
        assert body["count"] == 1
        assert body["logs"][0]["endpoint"] == "GET /posts"

    @patch("handlers.get_logs.boto3")
    def test_empty_results(self, mock_boto3):
        """空結果: 結果が0件の場合空配列を返す"""
        mock_client = _mock_logs_client(results=[])
        mock_boto3.client.return_value = mock_client

        resp = lambda_handler(_make_event(), FakeContext())
        assert resp["statusCode"] == 200
        body = json.loads(resp["body"])
        assert body["count"] == 0
        assert body["logs"] == []

    @patch("handlers.get_logs.boto3")
    def test_cloudwatch_error_returns_500(self, mock_boto3):
        """CloudWatch API エラー時に 500"""
        mock_client = _mock_logs_client(
            start_query_error=Exception("CW Logs unavailable")
        )
        mock_boto3.client.return_value = mock_client

        resp = lambda_handler(_make_event(), FakeContext())
        assert resp["statusCode"] == 500
        body = json.loads(resp["body"])
        assert "error" in body

    @patch("handlers.get_logs.boto3")
    def test_no_log_groups_returns_empty(self, mock_boto3):
        """ロググループが見つからない場合は空結果を返す"""
        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [{"logGroups": []}]
        mock_client.get_paginator.return_value = mock_paginator
        mock_boto3.client.return_value = mock_client

        resp = lambda_handler(_make_event(), FakeContext())
        assert resp["statusCode"] == 200
        body = json.loads(resp["body"])
        assert body["count"] == 0
        assert body["logs"] == []
