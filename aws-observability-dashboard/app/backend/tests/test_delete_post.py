"""DELETE /posts/:id ユニットテスト（PBI-005）"""

import json
import os
import unittest
from unittest.mock import MagicMock, patch

# テスト用環境変数を先に設定
os.environ["TABLE_NAME"] = "test-posts"
os.environ["AWS_DEFAULT_REGION"] = "ap-northeast-1"


class TestDeletePostHandler(unittest.TestCase):
    """delete_post Lambda ハンドラのユニットテスト。"""

    @patch("handlers.delete_post.table")
    def test_正常に投稿を削除できる(self, mock_table):
        """存在する ID を指定した場合、200 を返し削除が実行される。"""
        mock_item = {
            "id": "post-001",
            "title": "テスト投稿",
            "content": "テスト本文",
            "createdAt": "2026-03-16T10:00:00+00:00",
        }
        mock_table.get_item.return_value = {"Item": mock_item}
        mock_table.delete_item.return_value = {}

        from handlers.delete_post import lambda_handler

        event = {
            "httpMethod": "DELETE",
            "resource": "/posts/{id}",
            "pathParameters": {"id": "post-001"},
        }
        context = MagicMock()
        context.aws_request_id = "test-req-003"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertIn("削除しました", body["message"])
        mock_table.get_item.assert_called_once_with(Key={"id": "post-001"})
        mock_table.delete_item.assert_called_once_with(Key={"id": "post-001"})

    @patch("handlers.delete_post.table")
    def test_存在しないIDで404を返す(self, mock_table):
        """存在しない ID を指定した場合、404 を返し削除は実行されない。"""
        mock_table.get_item.return_value = {}

        from handlers.delete_post import lambda_handler

        event = {
            "httpMethod": "DELETE",
            "resource": "/posts/{id}",
            "pathParameters": {"id": "nonexistent-id"},
        }
        context = MagicMock()
        context.aws_request_id = "test-req-004"

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 404)
        body = json.loads(response["body"])
        self.assertIn("見つかりません", body["message"])
        mock_table.delete_item.assert_not_called()


if __name__ == "__main__":
    unittest.main()
