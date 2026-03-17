"""GET /posts/:id ユニットテスト（PBI-004）"""

import json
import os
import unittest
from unittest.mock import MagicMock, patch

# テスト用環境変数を先に設定
os.environ["TABLE_NAME"] = "test-posts"
os.environ["AWS_DEFAULT_REGION"] = "ap-northeast-1"


class TestGetPostHandler(unittest.TestCase):
    """get_post Lambda ハンドラのユニットテスト。"""

    @patch("handlers.get_post.table")
    def test_正常に投稿を取得できる(self, mock_table):
        """存在する ID を指定した場合、200 と投稿データを返す。"""
        mock_item = {
            "id": "post-001",
            "title": "テスト投稿",
            "content": "テスト本文",
            "createdAt": "2026-03-16T10:00:00+00:00",
        }
        mock_table.get_item.return_value = {"Item": mock_item}

        from handlers.get_post import lambda_handler

        event = {
            "httpMethod": "GET",
            "resource": "/posts/{id}",
            "pathParameters": {"id": "post-001"},
        }
        context = MagicMock()
        context.aws_request_id = "test-req-001"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["id"], "post-001")
        self.assertEqual(body["title"], "テスト投稿")
        mock_table.get_item.assert_called_once_with(Key={"id": "post-001"})

    @patch("handlers.get_post.table")
    def test_存在しないIDで404を返す(self, mock_table):
        """存在しない ID を指定した場合、404 を返す。"""
        mock_table.get_item.return_value = {}

        from handlers.get_post import lambda_handler

        event = {
            "httpMethod": "GET",
            "resource": "/posts/{id}",
            "pathParameters": {"id": "nonexistent-id"},
        }
        context = MagicMock()
        context.aws_request_id = "test-req-002"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 404)
        body = json.loads(response["body"])
        self.assertIn("見つかりません", body["message"])


if __name__ == "__main__":
    unittest.main()
