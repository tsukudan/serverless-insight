"""GET /posts/:id Lambda ハンドラ（PBI-004）

DynamoDB の posts テーブルから指定 ID の投稿を取得する。
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
    """指定 ID の投稿を取得する Lambda ハンドラ。"""
    try:
        post_id = event.get("pathParameters", {}).get("id", "")

        if not post_id:
            return {
                "statusCode": 400,
                "headers": CORS_HEADERS,
                "body": json.dumps(
                    {"message": "投稿 ID が指定されていません"}, ensure_ascii=False
                ),
            }

        response = table.get_item(Key={"id": post_id})
        item = response.get("Item")

        if not item:
            logger.warn("投稿が見つかりません", post_id=post_id)
            return {
                "statusCode": 404,
                "headers": CORS_HEADERS,
                "body": json.dumps(
                    {"message": "指定された投稿が見つかりません"}, ensure_ascii=False
                ),
            }

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps(item, ensure_ascii=False, default=str),
        }
    except Exception as exc:
        logger.error(
            "投稿詳細取得失敗",
            error_code="DDB_GET_FAILED",
            error_type=type(exc).__name__,
        )
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps(
                {"message": "投稿の取得に失敗しました"}, ensure_ascii=False
            ),
        }
