"""GET /posts ユニットテスト（PBI-002）"""

import json
import os
import unittest
from unittest.mock import MagicMock, patch

# テスト用環境変数を先に設定
os.environ["TABLE_NAME"] = "test-posts"
os.environ["AWS_DEFAULT_REGION"] = "ap-northeast-1"


class TestGetPostsHandler(unittest.TestCase):
    """get_posts Lambda ハンドラのユニットテスト。"""

    @patch("handlers.get_posts.table")
    def test_複数投稿をcreatedAt降順で返す(self, mock_table):
        """複数の投稿がある場合、createdAt の降順でソートされて返る。"""
        mock_items = [
            {
                "id": "post-001",
                "title": "古い投稿",
                "content": "本文1",
                "createdAt": "2026-03-15T10:00:00+00:00",
            },
            {
                "id": "post-002",
                "title": "新しい投稿",
                "content": "本文2",
                "createdAt": "2026-03-16T10:00:00+00:00",
            },
            {
                "id": "post-003",
                "title": "最新投稿",
                "content": "本文3",
                "createdAt": "2026-03-17T10:00:00+00:00",
            },
        ]
        mock_table.scan.return_value = {"Items": mock_items}

        from handlers.get_posts import lambda_handler

        event = {"httpMethod": "GET", "resource": "/posts"}
        context = MagicMock()
        context.aws_request_id = "test-req-001"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(len(body), 3)
        # 降順: 最新 → 古い
        self.assertEqual(body[0]["id"], "post-003")
        self.assertEqual(body[1]["id"], "post-002")
        self.assertEqual(body[2]["id"], "post-001")
        mock_table.scan.assert_called_once()

    @patch("handlers.get_posts.table")
    def test_投稿0件で空配列を返す(self, mock_table):
        """投稿が0件の場合、空配列が返る。"""
        mock_table.scan.return_value = {"Items": []}

        from handlers.get_posts import lambda_handler

        event = {"httpMethod": "GET", "resource": "/posts"}
        context = MagicMock()
        context.aws_request_id = "test-req-002"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body, [])
        mock_table.scan.assert_called_once()

    @patch("handlers.get_posts.table")
    def test_DynamoDBエラー時に500を返す(self, mock_table):
        """DynamoDB エラー時に 500 とエラーメッセージを返す。"""
        mock_table.scan.side_effect = Exception("DynamoDB connection error")

        from handlers.get_posts import lambda_handler

        event = {"httpMethod": "GET", "resource": "/posts"}
        context = MagicMock()
        context.aws_request_id = "test-req-003"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 500)
        body = json.loads(response["body"])
        self.assertIn("失敗", body["message"])


if __name__ == "__main__":
    unittest.main()
