"""CloudWatch ログ取得 Lambda ハンドラ（PBI-012）

GET /logs エンドポイント。
CloudWatch Logs Insights を使用してアプリケーションログを取得し、
レベル・エンドポイントのフィルタリング結果を返す。
"""

import json
import os
import time
from datetime import datetime, timezone, timedelta

import boto3

from shared.logger import StructuredLogger

logger = StructuredLogger(service="op-api")

RANGE_CONFIG = {
    "1h": {"hours": 1},
    "6h": {"hours": 6},
    "24h": {"hours": 24},
    "7d": {"hours": 168},
}

VALID_LEVELS = {"INFO", "WARN", "ERROR"}

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
}

MAX_RESULTS = 100
QUERY_POLL_INTERVAL = 0.5
QUERY_MAX_WAIT = 30


def _build_response(status_code, body):
    """HTTP レスポンスを構築する。"""
    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "body": json.dumps(body, ensure_ascii=False),
    }


def _parse_params(event):
    """クエリパラメータから range, level, endpoint を取得する。"""
    params = event.get("queryStringParameters") or {}
    time_range = params.get("range", "1h")
    level_filter = params.get("level")
    endpoint_filter = params.get("endpoint")

    if time_range not in RANGE_CONFIG:
        time_range = "1h"

    if level_filter and level_filter not in VALID_LEVELS:
        level_filter = None

    return time_range, level_filter, endpoint_filter


def _build_query(level_filter=None):
    """CloudWatch Logs Insights クエリを構築する。

    level_filter は VALID_LEVELS で検証済みの値のみ受け付ける。
    endpoint フィルタは Python 側で適用するためクエリには含めない。
    """
    parts = ["fields @timestamp, @message"]

    if level_filter:
        parts.append(f'| filter @message like /"level":"{level_filter}"/')

    parts.append("| sort @timestamp desc")
    parts.append(f"| limit {MAX_RESULTS}")

    return "\n".join(parts)


def _get_log_group_names(logs_client, prefix):
    """ロググループ名の一覧をプレフィックスで検索して返す。"""
    log_groups = []
    paginator = logs_client.get_paginator("describe_log_groups")
    for page in paginator.paginate(logGroupNamePrefix=prefix):
        for group in page.get("logGroups", []):
            log_groups.append(group["logGroupName"])
    return log_groups


def _parse_log_entry(message):
    """@message から JSON 構造化ログをパースする。"""
    try:
        data = json.loads(message)
        return {
            "timestamp": data.get("timestamp", ""),
            "level": data.get("level", ""),
            "endpoint": data.get("endpoint", ""),
            "requestId": data.get("requestId", ""),
            "message": data.get("message", ""),
            "statusCode": data.get("statusCode"),
            "durationMs": data.get("durationMs"),
            "errorCode": data.get("errorCode"),
        }
    except (json.JSONDecodeError, TypeError):
        return None


def _execute_query(logs_client, log_group_names, query, start_time, end_time):
    """CloudWatch Logs Insights クエリを実行し結果を返す。"""
    response = logs_client.start_query(
        logGroupNames=log_group_names,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
    )
    query_id = response["queryId"]

    elapsed = 0.0
    while elapsed < QUERY_MAX_WAIT:
        result = logs_client.get_query_results(queryId=query_id)
        status = result.get("status")
        if status == "Complete":
            return result.get("results", [])
        if status in ("Failed", "Cancelled", "Timeout"):
            raise RuntimeError(
                f"CloudWatch Logs Insights クエリ失敗: {status}"
            )
        time.sleep(QUERY_POLL_INTERVAL)
        elapsed += QUERY_POLL_INTERVAL

    raise RuntimeError("CloudWatch Logs Insights クエリタイムアウト")


def _process_results(raw_results, endpoint_filter=None):
    """Logs Insights の結果をパースしてログエントリのリストに変換する。"""
    logs = []
    for row in raw_results:
        message = None
        timestamp = None
        for field in row:
            if field["field"] == "@message":
                message = field["value"]
            elif field["field"] == "@timestamp":
                timestamp = field["value"]

        if message:
            entry = _parse_log_entry(message)
            if entry:
                if not entry["timestamp"] and timestamp:
                    entry["timestamp"] = timestamp

                # エンドポイントフィルタ（Python 側で部分一致）
                if endpoint_filter and endpoint_filter not in entry.get("endpoint", ""):
                    continue

                logs.append(entry)

    return logs


@logger.handler
def lambda_handler(event, context):
    """GET /logs Lambda ハンドラ。"""
    time_range, level_filter, endpoint_filter = _parse_params(event)
    config = RANGE_CONFIG[time_range]

    log_group_prefix = os.environ.get(
        "LOG_GROUP_PREFIX", "/aws/lambda/serverless-insight-demo-"
    )

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=config["hours"])

    logger.info("ログ取得開始")

    try:
        logs_client = boto3.client("logs")

        log_group_names = _get_log_group_names(logs_client, log_group_prefix)
        if not log_group_names:
            return _build_response(200, {
                "logs": [],
                "count": 0,
                "timeRange": time_range,
            })

        query = _build_query(level_filter)
        results = _execute_query(
            logs_client,
            log_group_names,
            query,
            start_time=int(start_time.timestamp()),
            end_time=int(now.timestamp()),
        )

        logs = _process_results(results, endpoint_filter)

        return _build_response(200, {
            "logs": logs,
            "count": len(logs),
            "timeRange": time_range,
        })

    except Exception as exc:
        logger.error(
            "CloudWatch ログ取得失敗",
            error_code="CLOUDWATCH_LOGS_API_ERROR",
            error_type=type(exc).__name__,
        )
        return _build_response(500, {"error": "ログ取得に失敗しました"})
