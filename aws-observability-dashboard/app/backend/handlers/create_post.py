"""POST /posts Lambda ハンドラ（PBI-003）

DynamoDB の posts テーブルに新しい投稿を作成する。
"""

import json
import os
import uuid
from datetime import datetime, timezone

import boto3

from shared.logger import StructuredLogger

logger = StructuredLogger(service="demo-api")

TABLE_NAME = os.environ.get("TABLE_NAME", "posts")

CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
}

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


@logger.handler
def lambda_handler(event, context):
    """投稿を作成する Lambda ハンドラ。"""
    try:
        # リクエストボディのパース
        body = event.get("body", "")
        if isinstance(body, str):
            body = json.loads(body) if body else {}

        title = body.get("title", "")
        post_body = body.get("body", "")

        # バリデーション
        if not title or not title.strip():
            return {
                "statusCode": 400,
                "headers": CORS_HEADERS,
                "body": json.dumps(
                    {"message": "title は必須です"}, ensure_ascii=False
                ),
            }

        if not post_body or not post_body.strip():
            return {
                "statusCode": 400,
                "headers": CORS_HEADERS,
                "body": json.dumps(
                    {"message": "body は必須です"}, ensure_ascii=False
                ),
            }

        # 投稿データの作成
        now = datetime.now(timezone.utc).isoformat()
        item = {
            "id": str(uuid.uuid4()),
            "title": title,
            "body": post_body,
            "createdAt": now,
            "updatedAt": now,
        }

        # DynamoDB に保存
        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "headers": CORS_HEADERS,
            "body": json.dumps(item, ensure_ascii=False, default=str),
        }
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps(
                {"message": "リクエストボディの JSON が不正です"}, ensure_ascii=False
            ),
        }
    except Exception as exc:
        logger.error(
            "投稿作成失敗",
            error_code="DDB_PUT_FAILED",
            error_type=type(exc).__name__,
        )
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps(
                {"message": "投稿の作成に失敗しました"}, ensure_ascii=False
            ),
        }
