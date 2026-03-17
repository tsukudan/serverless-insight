"""Lambda 構造化ログモジュール（PBI-006）

JSON 形式の構造化ログを出力する共通モジュール。
Python 標準ライブラリのみ使用（外部依存なし）。

必須フィールド: timestamp (ISO 8601), level, service, endpoint, requestId, message
リクエスト完了ログ追加フィールド: statusCode, durationMs
エラーログ追加フィールド: errorCode, errorType

使用例::

    from shared.logger import StructuredLogger

    logger = StructuredLogger(service="demo-api")
    logger.set_context(endpoint="GET /posts", request_id="abc-123")
    logger.info("投稿一覧取得開始")
    logger.info("投稿一覧取得完了", status_code=200, duration_ms=42)
    logger.error("投稿作成失敗", error_code="DDB_WRITE_FAILED", error_type="DynamoDBError")
"""

import json
import sys
import time
import functools
from datetime import datetime, timezone


class StructuredLogger:
    """コンテキストを保持する構造化ログクラス。"""

    def __init__(self, service: str) -> None:
        self._service = service
        self._endpoint: str = ""
        self._request_id: str = ""

    def set_context(self, endpoint: str = "", request_id: str = "") -> None:
        """リクエストコンテキストを設定する。"""
        if endpoint:
            self._endpoint = endpoint
        if request_id:
            self._request_id = request_id

    def clear_context(self) -> None:
        """リクエストコンテキストをリセットする。"""
        self._endpoint = ""
        self._request_id = ""

    # -----------------------------------------------------------------
    # ログ出力メソッド
    # -----------------------------------------------------------------

    def info(self, message: str, **kwargs) -> None:
        self._log("INFO", message, **kwargs)

    def warn(self, message: str, **kwargs) -> None:
        self._log("WARN", message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self._log("ERROR", message, **kwargs)

    # -----------------------------------------------------------------
    # Lambda ハンドラデコレータ
    # -----------------------------------------------------------------

    def handler(self, func):
        """Lambda ハンドラデコレータ。

        リクエスト開始・完了ログを自動出力し、処理時間を計測する。
        デコレートされた関数は ``(event, context)`` を受け取る Lambda ハンドラである想定。
        """

        @functools.wraps(func)
        def wrapper(event, context):
            # コンテキスト設定
            request_id = getattr(context, "aws_request_id", "") if context else ""
            http_method = ""
            resource = ""
            if isinstance(event, dict):
                http_method = event.get("httpMethod", "")
                resource = event.get("resource", "")
            endpoint = f"{http_method} {resource}" if http_method else ""

            self.set_context(endpoint=endpoint, request_id=request_id)
            self.info("リクエスト開始")

            start = time.time()
            try:
                result = func(event, context)
                duration_ms = round((time.time() - start) * 1000)
                status_code = result.get("statusCode", 0) if isinstance(result, dict) else 0
                self.info(
                    "リクエスト完了",
                    status_code=status_code,
                    duration_ms=duration_ms,
                )
                return result
            except Exception as exc:
                duration_ms = round((time.time() - start) * 1000)
                self.error(
                    "リクエスト失敗",
                    error_code="UNHANDLED_EXCEPTION",
                    error_type=type(exc).__name__,
                )
                raise
            finally:
                self.clear_context()

        return wrapper

    # -----------------------------------------------------------------
    # 内部メソッド
    # -----------------------------------------------------------------

    def _log(self, level: str, message: str, **kwargs) -> None:
        """JSON 構造化ログを標準出力に書き込む。"""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "service": self._service,
            "endpoint": self._endpoint,
            "requestId": self._request_id,
            "message": message,
        }

        # リクエスト完了ログ追加フィールド
        if "status_code" in kwargs:
            record["statusCode"] = kwargs["status_code"]
        if "duration_ms" in kwargs:
            record["durationMs"] = kwargs["duration_ms"]

        # エラーログ追加フィールド
        if "error_code" in kwargs:
            record["errorCode"] = kwargs["error_code"]
        if "error_type" in kwargs:
            record["errorType"] = kwargs["error_type"]

        print(json.dumps(record, ensure_ascii=False), file=sys.stdout, flush=True)
