"""CloudWatch メトリクス取得 Lambda ハンドラ（PBI-011）

GET /metrics エンドポイント。
CloudWatch の get_metric_data API を使用して API Gateway メトリクスを取得し、
サマリー・時系列・エンドポイント別の集計結果を返す。
"""

import json
import os
from datetime import datetime, timezone, timedelta

import boto3

from shared.logger import StructuredLogger

logger = StructuredLogger(service="op-api")

# 時間範囲ごとの設定
RANGE_CONFIG = {
    "1h": {"hours": 1, "period": 60},
    "6h": {"hours": 6, "period": 300},
    "24h": {"hours": 24, "period": 300},
    "7d": {"hours": 168, "period": 3600},
}

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
}


def _build_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "body": json.dumps(body, ensure_ascii=False),
    }


def _parse_params(event: dict) -> tuple:
    """クエリパラメータから range と endpoint を取得する。"""
    params = event.get("queryStringParameters") or {}
    time_range = params.get("range", "1h")
    endpoint_filter = params.get("endpoint")

    if time_range not in RANGE_CONFIG:
        time_range = "1h"

    return time_range, endpoint_filter


def _build_metric_queries(api_name: str, period: int) -> list:
    """CloudWatch MetricDataQueries を構築する。"""
    dimensions = [{"Name": "ApiName", "Value": api_name}]
    namespace = "AWS/ApiGateway"

    queries = [
        {
            "Id": "request_count",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": "Count",
                    "Dimensions": dimensions,
                },
                "Period": period,
                "Stat": "Sum",
            },
            "ReturnData": True,
        },
        {
            "Id": "error_4xx",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": "4XXError",
                    "Dimensions": dimensions,
                },
                "Period": period,
                "Stat": "Sum",
            },
            "ReturnData": True,
        },
        {
            "Id": "error_5xx",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": "5XXError",
                    "Dimensions": dimensions,
                },
                "Period": period,
                "Stat": "Sum",
            },
            "ReturnData": True,
        },
        {
            "Id": "latency_avg",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": "Latency",
                    "Dimensions": dimensions,
                },
                "Period": period,
                "Stat": "Average",
            },
            "ReturnData": True,
        },
        {
            "Id": "latency_p95",
            "MetricStat": {
                "Metric": {
                    "Namespace": namespace,
                    "MetricName": "Latency",
                    "Dimensions": dimensions,
                },
                "Period": period,
                "Stat": "p95",
            },
            "ReturnData": True,
        },
    ]
    return queries


def _extract_results(metric_results: list) -> dict:
    """get_metric_data の結果を ID ごとの辞書に変換する。"""
    results = {}
    for result in metric_results:
        results[result["Id"]] = {
            "timestamps": result.get("Timestamps", []),
            "values": result.get("Values", []),
        }
    return results


def _build_time_series(results: dict) -> list:
    """時系列データを構築する。"""
    count_data = results.get("request_count", {"timestamps": [], "values": []})
    error_4xx = results.get("error_4xx", {"timestamps": [], "values": []})
    error_5xx = results.get("error_5xx", {"timestamps": [], "values": []})
    latency_avg = results.get("latency_avg", {"timestamps": [], "values": []})

    # タイムスタンプをキーにしてデータをマージ
    ts_map = {}
    for i, ts in enumerate(count_data["timestamps"]):
        key = ts.isoformat() if isinstance(ts, datetime) else str(ts)
        ts_map[key] = {
            "timestamp": key,
            "requests": int(count_data["values"][i]) if i < len(count_data["values"]) else 0,
            "errors": 0,
            "avgLatency": 0.0,
        }

    for i, ts in enumerate(error_4xx["timestamps"]):
        key = ts.isoformat() if isinstance(ts, datetime) else str(ts)
        if key in ts_map:
            ts_map[key]["errors"] += int(error_4xx["values"][i]) if i < len(error_4xx["values"]) else 0

    for i, ts in enumerate(error_5xx["timestamps"]):
        key = ts.isoformat() if isinstance(ts, datetime) else str(ts)
        if key in ts_map:
            ts_map[key]["errors"] += int(error_5xx["values"][i]) if i < len(error_5xx["values"]) else 0

    for i, ts in enumerate(latency_avg["timestamps"]):
        key = ts.isoformat() if isinstance(ts, datetime) else str(ts)
        if key in ts_map:
            ts_map[key]["avgLatency"] = round(latency_avg["values"][i], 1) if i < len(latency_avg["values"]) else 0.0

    # タイムスタンプ昇順でソート
    time_series = sorted(ts_map.values(), key=lambda x: x["timestamp"])
    return time_series


def _build_summary(results: dict) -> dict:
    """サマリーデータを構築する。"""
    count_values = results.get("request_count", {"values": []})["values"]
    error_4xx_values = results.get("error_4xx", {"values": []})["values"]
    error_5xx_values = results.get("error_5xx", {"values": []})["values"]
    latency_avg_values = results.get("latency_avg", {"values": []})["values"]
    latency_p95_values = results.get("latency_p95", {"values": []})["values"]

    total_requests = int(sum(count_values)) if count_values else 0
    total_errors = (
        int(sum(error_4xx_values)) + int(sum(error_5xx_values))
        if error_4xx_values or error_5xx_values
        else 0
    )
    error_rate = round((total_errors / total_requests) * 100, 1) if total_requests > 0 else 0.0
    avg_latency = round(sum(latency_avg_values) / len(latency_avg_values), 1) if latency_avg_values else 0.0
    p95_latency = round(max(latency_p95_values), 1) if latency_p95_values else 0.0

    return {
        "totalRequests": total_requests,
        "errorRate": error_rate,
        "avgLatency": avg_latency,
        "p95Latency": p95_latency,
    }


def _build_endpoints(results: dict, api_name: str) -> list:
    """エンドポイント別データを構築する。

    NOTE: CloudWatch の ApiName ディメンションだけでは個別エンドポイントの
    分解ができないため、API 全体を1エンドポイントとして集計する。
    将来的に Resource/Method ディメンションへの対応を検討。
    """
    summary = _build_summary(results)
    total = summary["totalRequests"]
    errors = int(total * summary["errorRate"] / 100) if total > 0 else 0
    success_rate = round(100 - summary["errorRate"], 1)

    return [
        {
            "endpoint": f"ALL ({api_name})",
            "requests": total,
            "successRate": success_rate,
            "avgLatency": summary["avgLatency"],
            "p95Latency": summary["p95Latency"],
            "errors": errors,
        }
    ]


@logger.handler
def lambda_handler(event, context):
    """GET /metrics Lambda ハンドラ。"""
    time_range, endpoint_filter = _parse_params(event)
    config = RANGE_CONFIG[time_range]

    api_name = os.environ.get("API_NAME", "demo-app-api")

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=config["hours"])
    end_time = now
    period = config["period"]

    logger.info(
        "メトリクス取得開始",
        time_range=time_range,
        api_name=api_name,
        period=period,
    )

    try:
        cw_client = boto3.client("cloudwatch")
        queries = _build_metric_queries(api_name, period)

        response = cw_client.get_metric_data(
            MetricDataQueries=queries,
            StartTime=start_time,
            EndTime=end_time,
        )

        results = _extract_results(response.get("MetricDataResults", []))
        summary = _build_summary(results)
        time_series = _build_time_series(results)
        endpoints = _build_endpoints(results, api_name)

        # endpoint フィルタ（将来の拡張用、現状は全件返却）
        if endpoint_filter:
            endpoints = [e for e in endpoints if endpoint_filter in e["endpoint"]]

        body = {
            "summary": summary,
            "timeSeries": time_series,
            "endpoints": endpoints,
            "timeRange": time_range,
        }

        return _build_response(200, body)

    except Exception as exc:
        logger.error(
            "CloudWatch メトリクス取得失敗",
            error_code="CLOUDWATCH_API_ERROR",
            error_type=type(exc).__name__,
        )
        return _build_response(500, {"error": "メトリクス取得に失敗しました"})
