"""StructuredLogger ユニットテスト（PBI-006）"""

import json
import unittest
from io import StringIO
from unittest.mock import patch

from shared.logger import StructuredLogger


REQUIRED_FIELDS = {"timestamp", "level", "service", "endpoint", "requestId", "message"}


class TestStructuredLoggerBasicLevels(unittest.TestCase):
    """INFO / WARN / ERROR の各ログレベルが正しく出力されることを検証する。"""

    def setUp(self):
        self.logger = StructuredLogger(service="test-service")
        self.logger.set_context(endpoint="GET /test", request_id="req-001")

    def _capture_log(self, method, message, **kwargs):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            method(message, **kwargs)
            return json.loads(mock_stdout.getvalue().strip())

    def test_info_log(self):
        record = self._capture_log(self.logger.info, "情報ログ")
        self.assertEqual(record["level"], "INFO")
        self.assertEqual(record["message"], "情報ログ")

    def test_warn_log(self):
        record = self._capture_log(self.logger.warn, "警告ログ")
        self.assertEqual(record["level"], "WARN")
        self.assertEqual(record["message"], "警告ログ")

    def test_error_log(self):
        record = self._capture_log(self.logger.error, "エラーログ")
        self.assertEqual(record["level"], "ERROR")
        self.assertEqual(record["message"], "エラーログ")


class TestRequiredFields(unittest.TestCase):
    """必須フィールドが全て含まれていることを検証する。"""

    def test_all_required_fields_present(self):
        logger = StructuredLogger(service="svc")
        logger.set_context(endpoint="POST /items", request_id="r-123")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.info("テスト")
            record = json.loads(mock_stdout.getvalue().strip())

        self.assertTrue(REQUIRED_FIELDS.issubset(record.keys()))
        self.assertEqual(record["service"], "svc")
        self.assertEqual(record["endpoint"], "POST /items")
        self.assertEqual(record["requestId"], "r-123")

    def test_timestamp_iso8601(self):
        logger = StructuredLogger(service="svc")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.info("ts test")
            record = json.loads(mock_stdout.getvalue().strip())

        # ISO 8601 タイムスタンプの基本検証
        ts = record["timestamp"]
        self.assertIn("T", ts)
        self.assertTrue(ts.endswith("+00:00") or ts.endswith("Z"))


class TestRequestCompletionFields(unittest.TestCase):
    """statusCode / durationMs の追加フィールドを検証する。"""

    def test_status_code_and_duration(self):
        logger = StructuredLogger(service="api")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.info("完了", status_code=200, duration_ms=35)
            record = json.loads(mock_stdout.getvalue().strip())

        self.assertEqual(record["statusCode"], 200)
        self.assertEqual(record["durationMs"], 35)

    def test_no_extra_fields_without_kwargs(self):
        logger = StructuredLogger(service="api")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.info("通常ログ")
            record = json.loads(mock_stdout.getvalue().strip())

        self.assertNotIn("statusCode", record)
        self.assertNotIn("durationMs", record)


class TestErrorFields(unittest.TestCase):
    """errorCode / errorType の追加フィールドを検証する。"""

    def test_error_code_and_type(self):
        logger = StructuredLogger(service="api")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.error(
                "書き込み失敗",
                error_code="DDB_WRITE_FAILED",
                error_type="DynamoDBError",
            )
            record = json.loads(mock_stdout.getvalue().strip())

        self.assertEqual(record["errorCode"], "DDB_WRITE_FAILED")
        self.assertEqual(record["errorType"], "DynamoDBError")

    def test_no_error_fields_without_kwargs(self):
        logger = StructuredLogger(service="api")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.error("汎用エラー")
            record = json.loads(mock_stdout.getvalue().strip())

        self.assertNotIn("errorCode", record)
        self.assertNotIn("errorType", record)


class TestContextManagement(unittest.TestCase):
    """コンテキストの設定・リセットを検証する。"""

    def test_set_context(self):
        logger = StructuredLogger(service="ctx")
        logger.set_context(endpoint="GET /ctx", request_id="ctx-001")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.info("ctx test")
            record = json.loads(mock_stdout.getvalue().strip())

        self.assertEqual(record["endpoint"], "GET /ctx")
        self.assertEqual(record["requestId"], "ctx-001")

    def test_clear_context(self):
        logger = StructuredLogger(service="ctx")
        logger.set_context(endpoint="GET /ctx", request_id="ctx-001")
        logger.clear_context()
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.info("cleared")
            record = json.loads(mock_stdout.getvalue().strip())

        self.assertEqual(record["endpoint"], "")
        self.assertEqual(record["requestId"], "")

    def test_partial_context_update(self):
        logger = StructuredLogger(service="ctx")
        logger.set_context(endpoint="GET /a", request_id="r1")
        logger.set_context(request_id="r2")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            logger.info("partial")
            record = json.loads(mock_stdout.getvalue().strip())

        self.assertEqual(record["endpoint"], "GET /a")
        self.assertEqual(record["requestId"], "r2")


class TestHandlerDecorator(unittest.TestCase):
    """Lambda ハンドラデコレータの動作を検証する。"""

    def test_decorator_logs_start_and_completion(self):
        logger = StructuredLogger(service="demo")

        @logger.handler
        def my_handler(event, context):
            return {"statusCode": 200, "body": "ok"}

        class FakeContext:
            aws_request_id = "fake-req-id"

        event = {"httpMethod": "GET", "resource": "/posts"}

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            result = my_handler(event, FakeContext())

        self.assertEqual(result["statusCode"], 200)

        lines = mock_stdout.getvalue().strip().split("\n")
        self.assertEqual(len(lines), 2)

        start_record = json.loads(lines[0])
        self.assertEqual(start_record["message"], "リクエスト開始")
        self.assertEqual(start_record["endpoint"], "GET /posts")
        self.assertEqual(start_record["requestId"], "fake-req-id")

        end_record = json.loads(lines[1])
        self.assertEqual(end_record["message"], "リクエスト完了")
        self.assertEqual(end_record["statusCode"], 200)
        self.assertIn("durationMs", end_record)

    def test_decorator_logs_error_on_exception(self):
        logger = StructuredLogger(service="demo")

        @logger.handler
        def bad_handler(event, context):
            raise ValueError("テストエラー")

        class FakeContext:
            aws_request_id = "err-req"

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            with self.assertRaises(ValueError):
                bad_handler({"httpMethod": "POST", "resource": "/items"}, FakeContext())

        lines = mock_stdout.getvalue().strip().split("\n")
        self.assertEqual(len(lines), 2)

        err_record = json.loads(lines[1])
        self.assertEqual(err_record["message"], "リクエスト失敗")
        self.assertEqual(err_record["errorCode"], "UNHANDLED_EXCEPTION")
        self.assertEqual(err_record["errorType"], "ValueError")

    def test_decorator_clears_context_after_execution(self):
        logger = StructuredLogger(service="demo")

        @logger.handler
        def handler(event, context):
            return {"statusCode": 200}

        class FakeContext:
            aws_request_id = "req-clear"

        with patch("sys.stdout", new_callable=StringIO):
            handler({"httpMethod": "GET", "resource": "/x"}, FakeContext())

        # デコレータ完了後、コンテキストがクリアされていること
        self.assertEqual(logger._endpoint, "")
        self.assertEqual(logger._request_id, "")


if __name__ == "__main__":
    unittest.main()
