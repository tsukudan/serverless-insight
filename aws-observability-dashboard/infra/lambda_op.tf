###############################################################################
# Lambda 関数定義 — Observability Platform (OP)
###############################################################################

# =============================================================================
# デプロイパッケージ（ZIP アーカイブ）
# =============================================================================

data "archive_file" "op_backend" {
  type        = "zip"
  source_dir  = "${path.module}/../app/backend-op"
  output_path = "${path.module}/../app/backend-op/deploy.zip"
  excludes    = ["tests", "__pycache__", "deploy.zip", ".pytest_cache"]
}

# =============================================================================
# Lambda 関数
# =============================================================================

# --- GET /metrics — CloudWatch メトリクス取得 ---------------------------------
resource "aws_lambda_function" "op_get_metrics" {
  function_name    = "${var.project_name}-op-get_metrics"
  runtime          = "python3.12"
  handler          = "handlers/get_metrics.lambda_handler"
  role             = aws_iam_role.op_lambda_role.arn
  filename         = data.archive_file.op_backend.output_path
  source_code_hash = data.archive_file.op_backend.output_base64sha256
  timeout          = 30

  environment {
    variables = {
      API_NAME = var.demo_api_name
    }
  }

  tags = {
    Name = "${var.project_name}-op-get_metrics"
  }
}

# --- GET /logs — CloudWatch ログ取得 ------------------------------------------
resource "aws_lambda_function" "op_get_logs" {
  function_name    = "${var.project_name}-op-get_logs"
  runtime          = "python3.12"
  handler          = "handlers/get_logs.lambda_handler"
  role             = aws_iam_role.op_lambda_role.arn
  filename         = data.archive_file.op_backend.output_path
  source_code_hash = data.archive_file.op_backend.output_base64sha256
  timeout          = 30

  environment {
    variables = {
      LOG_GROUP_PREFIX = "/aws/lambda/${var.project_name}-demo-"
    }
  }

  tags = {
    Name = "${var.project_name}-op-get_logs"
  }
}

# =============================================================================
# Lambda 実行権限（API Gateway → Lambda）
# =============================================================================

resource "aws_lambda_permission" "op_get_metrics" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.op_get_metrics.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.op.execution_arn}/*/GET/metrics"
}

resource "aws_lambda_permission" "op_get_logs" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.op_get_logs.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.op.execution_arn}/*/GET/logs"
}

# =============================================================================
# API Gateway デプロイメント & ステージ
# =============================================================================

resource "aws_api_gateway_deployment" "op" {
  rest_api_id = aws_api_gateway_rest_api.op.id

  depends_on = [
    aws_api_gateway_integration.op_get_metrics,
    aws_api_gateway_integration.op_get_logs,
    aws_api_gateway_integration.op_options_metrics,
    aws_api_gateway_integration.op_options_logs,
  ]

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.op_metrics,
      aws_api_gateway_resource.op_logs,
      aws_api_gateway_method.op_get_metrics,
      aws_api_gateway_method.op_get_logs,
      aws_api_gateway_integration.op_get_metrics,
      aws_api_gateway_integration.op_get_logs,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "op" {
  deployment_id = aws_api_gateway_deployment.op.id
  rest_api_id   = aws_api_gateway_rest_api.op.id
  stage_name    = var.op_api_stage_name

  tags = {
    Name = "${var.project_name}-op-${var.op_api_stage_name}"
  }
}
