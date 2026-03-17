"""GetMetrics ハンドラ スモークテスト（DAY3）

DAY4 で伊藤が本格テスト（タスク 11-6）を実装予定。
ここでは基本的な動作確認のみ行う。
"""

import json
import os
import sys
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from handlers.get_metrics import (
    lambda_handler,
    RANGE_CONFIG,
    _parse_params,
    _build_metric_queries,
    _build_summary,
    _build_time_series,
    _build_response,
)


# ---------------------------------------------------------------------------
# ヘルパー
# ---------------------------------------------------------------------------

class FakeContext:
    aws_request_id = "test-request-id-001"


def _make_event(range_val=None, endpoint=None):
    params = {}
    if range_val is not None:
        params["range"] = range_val
    if endpoint is not None:
        params["endpoint"] = endpoint
    return {
        "httpMethod": "GET",
        "resource": "/metrics",
        "queryStringParameters": params if params else None,
    }


# ---------------------------------------------------------------------------
# テスト: パラメータ解析
# ---------------------------------------------------------------------------

class TestParseParams:
    def test_default_range(self):
        time_range, ep = _parse_params(_make_event())
        assert time_range == "1h"
        assert ep is None

    def test_valid_range(self):
        for r in ("1h", "6h", "24h", "7d"):
            time_range, _ = _parse_params(_make_event(range_val=r))
            assert time_range == r

    def test_invalid_range_falls_back(self):
        time_range, _ = _parse_params(_make_event(range_val="99h"))
        assert time_range == "1h"

    def test_endpoint_filter(self):
        _, ep = _parse_params(_make_event(endpoint="GET /posts"))
        assert ep == "GET /posts"


# ---------------------------------------------------------------------------
# テスト: RANGE_CONFIG
# ---------------------------------------------------------------------------

class TestRangeConfig:
    def test_all_keys_exist(self):
        for key in ("1h", "6h", "24h", "7d"):
            assert key in RANGE_CONFIG
            assert "hours" in RANGE_CONFIG[key]
            assert "period" in RANGE_CONFIG[key]

    def test_period_values(self):
        assert RANGE_CONFIG["1h"]["period"] == 60
        assert RANGE_CONFIG["6h"]["period"] == 300
        assert RANGE_CONFIG["24h"]["period"] == 300
        assert RANGE_CONFIG["7d"]["period"] == 3600


# ---------------------------------------------------------------------------
# テスト: メトリクスクエリ構築
# ---------------------------------------------------------------------------

class TestBuildMetricQueries:
    def test_returns_five_queries(self):
        queries = _build_metric_queries("test-api", 60)
        assert len(queries) == 5

    def test_query_ids(self):
        queries = _build_metric_queries("test-api", 60)
        ids = {q["Id"] for q in queries}
        assert ids == {"request_count", "error_4xx", "error_5xx", "latency_avg", "latency_p95"}

    def test_dimensions(self):
        queries = _build_metric_queries("my-api", 300)
        for q in queries:
            dims = q["MetricStat"]["Metric"]["Dimensions"]
            assert dims == [{"Name": "ApiName", "Value": "my-api"}]


# ---------------------------------------------------------------------------
# テスト: サマリー構築
# ---------------------------------------------------------------------------

class TestBuildSummary:
    def test_empty_results(self):
        results = {
            "request_count": {"timestamps": [], "values": []},
            "error_4xx": {"timestamps": [], "values": []},
            "error_5xx": {"timestamps": [], "values": []},
            "latency_avg": {"timestamps": [], "values": []},
            "latency_p95": {"timestamps": [], "values": []},
        }
        summary = _build_summary(results)
        assert summary["totalRequests"] == 0
        assert summary["errorRate"] == 0.0
        assert summary["avgLatency"] == 0.0
        assert summary["p95Latency"] == 0.0

    def test_with_data(self):
        results = {
            "request_count": {"timestamps": [], "values": [100, 200]},
            "error_4xx": {"timestamps": [], "values": [2, 3]},
            "error_5xx": {"timestamps": [], "values": [1, 0]},
            "latency_avg": {"timestamps": [], "values": [100.0, 200.0]},
            "latency_p95": {"timestamps": [], "values": [300.0, 400.0]},
        }
        summary = _build_summary(results)
        assert summary["totalRequests"] == 300
        assert summary["errorRate"] == 2.0  # 6/300 * 100
        assert summary["avgLatency"] == 150.0
        assert summary["p95Latency"] == 400.0


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
    @patch("handlers.get_metrics.boto3")
    def test_success_response(self, mock_boto3):
        now = datetime(2026, 3, 17, 10, 0, 0, tzinfo=timezone.utc)
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        mock_client.get_metric_data.return_value = {
            "MetricDataResults": [
                {"Id": "request_count", "Timestamps": [now], "Values": [100.0]},
                {"Id": "error_4xx", "Timestamps": [now], "Values": [2.0]},
                {"Id": "error_5xx", "Timestamps": [now], "Values": [1.0]},
                {"Id": "latency_avg", "Timestamps": [now], "Values": [120.5]},
                {"Id": "latency_p95", "Timestamps": [now], "Values": [350.0]},
            ]
        }

        event = _make_event(range_val="1h")
        resp = lambda_handler(event, FakeContext())

        assert resp["statusCode"] == 200
        body = json.loads(resp["body"])
        assert "summary" in body
        assert "timeSeries" in body
        assert "endpoints" in body
        assert body["timeRange"] == "1h"
        assert body["summary"]["totalRequests"] == 100

    @patch("handlers.get_metrics.boto3")
    def test_cloudwatch_error_returns_500(self, mock_boto3):
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        mock_client.get_metric_data.side_effect = Exception("CW unavailable")

        event = _make_event()
        resp = lambda_handler(event, FakeContext())

        assert resp["statusCode"] == 500
        body = json.loads(resp["body"])
        assert "error" in body
