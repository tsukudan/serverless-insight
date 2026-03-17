"""POST /posts ユニットテスト（PBI-003）"""

import json
import os
import unittest
from unittest.mock import MagicMock, patch

# テスト用環境変数を先に設定
os.environ["TABLE_NAME"] = "test-posts"
os.environ["AWS_DEFAULT_REGION"] = "ap-northeast-1"


class TestCreatePostHandler(unittest.TestCase):
    """create_post Lambda ハンドラのユニットテスト。"""

    @patch("handlers.create_post.uuid.uuid4", return_value="test-uuid-001")
    @patch("handlers.create_post.table")
    def test_正常に投稿を作成できる(self, mock_table, mock_uuid):
        """title と body を指定した場合、201 と作成された投稿データを返す。"""
        mock_table.put_item.return_value = {}

        from handlers.create_post import lambda_handler

        event = {
            "httpMethod": "POST",
            "resource": "/posts",
            "body": json.dumps({"title": "テスト投稿", "body": "テスト本文"}),
        }
        context = MagicMock()
        context.aws_request_id = "test-req-001"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 201)
        body = json.loads(response["body"])
        self.assertEqual(body["id"], "test-uuid-001")
        self.assertEqual(body["title"], "テスト投稿")
        self.assertEqual(body["body"], "テスト本文")
        self.assertIn("createdAt", body)
        self.assertIn("updatedAt", body)
        mock_table.put_item.assert_called_once()

    @patch("handlers.create_post.table")
    def test_titleが空文字の場合400を返す(self, mock_table):
        """title が空文字の場合、400 を返す。"""
        from handlers.create_post import lambda_handler

        event = {
            "httpMethod": "POST",
            "resource": "/posts",
            "body": json.dumps({"title": "", "body": "テスト本文"}),
        }
        context = MagicMock()
        context.aws_request_id = "test-req-002"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertIn("title", body["message"])
        mock_table.put_item.assert_not_called()

    @patch("handlers.create_post.table")
    def test_bodyが空文字の場合400を返す(self, mock_table):
        """body が空文字の場合、400 を返す。"""
        from handlers.create_post import lambda_handler

        event = {
            "httpMethod": "POST",
            "resource": "/posts",
            "body": json.dumps({"title": "テスト投稿", "body": ""}),
        }
        context = MagicMock()
        context.aws_request_id = "test-req-003"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertIn("body", body["message"])
        mock_table.put_item.assert_not_called()

    @patch("handlers.create_post.table")
    def test_bodyが未指定の場合400を返す(self, mock_table):
        """body が未指定の場合、400 を返す。"""
        from handlers.create_post import lambda_handler

        event = {
            "httpMethod": "POST",
            "resource": "/posts",
            "body": json.dumps({"title": "テスト投稿"}),
        }
        context = MagicMock()
        context.aws_request_id = "test-req-004"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertIn("body", body["message"])
        mock_table.put_item.assert_not_called()

    @patch("handlers.create_post.table")
    def test_DynamoDBエラー時に500を返す(self, mock_table):
        """DynamoDB エラーが発生した場合、500 を返す。"""
        mock_table.put_item.side_effect = Exception("DynamoDB error")

        from handlers.create_post import lambda_handler

        event = {
            "httpMethod": "POST",
            "resource": "/posts",
            "body": json.dumps({"title": "テスト投稿", "body": "テスト本文"}),
        }
        context = MagicMock()
        context.aws_request_id = "test-req-005"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 500)
        body = json.loads(response["body"])
        self.assertIn("失敗", body["message"])


if __name__ == "__main__":
    unittest.main()
