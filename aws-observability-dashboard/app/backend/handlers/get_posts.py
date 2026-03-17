"""GET /posts Lambda ハンドラ（PBI-002）

DynamoDB の posts テーブルから全件取得し、createdAt の降順で返す。
"""

import json
import os

import boto3

from shared.logger import StructuredLogger

logger = StructuredLogger(service="demo-api")

TABLE_NAME = os.environ.get("TABLE_NAME", "posts")

CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
}

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


@logger.handler
def lambda_handler(event, context):
    """投稿一覧を取得する Lambda ハンドラ。"""
    try:
        response = table.scan()
        items = response.get("Items", [])

        # createdAt の降順でソート（フィールドが無い場合は末尾へ）
        items.sort(key=lambda x: x.get("createdAt", ""), reverse=True)

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps(items, ensure_ascii=False, default=str),
        }
    except Exception as exc:
        logger.error(
            "投稿一覧取得失敗",
            error_code="DDB_SCAN_FAILED",
            error_type=type(exc).__name__,
        )
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps(
                {"message": "投稿一覧の取得に失敗しました"}, ensure_ascii=False
            ),
        }
