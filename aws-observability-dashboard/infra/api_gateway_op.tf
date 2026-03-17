###############################################################################
# API Gateway REST API 定義 — Observability Platform (OP)
###############################################################################

resource "aws_api_gateway_rest_api" "op" {
  name        = var.op_api_name
  description = var.op_api_description

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# =============================================================================
# リソース定義
# =============================================================================

# /metrics
resource "aws_api_gateway_resource" "op_metrics" {
  rest_api_id = aws_api_gateway_rest_api.op.id
  parent_id   = aws_api_gateway_rest_api.op.root_resource_id
  path_part   = "metrics"
}

# /logs
resource "aws_api_gateway_resource" "op_logs" {
  rest_api_id = aws_api_gateway_rest_api.op.id
  parent_id   = aws_api_gateway_rest_api.op.root_resource_id
  path_part   = "logs"
}

# =============================================================================
# /metrics メソッド
# =============================================================================

# GET /metrics — CloudWatch メトリクス取得
resource "aws_api_gateway_method" "op_get_metrics" {
  rest_api_id   = aws_api_gateway_rest_api.op.id
  resource_id   = aws_api_gateway_resource.op_metrics.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "op_get_metrics" {
  rest_api_id             = aws_api_gateway_rest_api.op.id
  resource_id             = aws_api_gateway_resource.op_metrics.id
  http_method             = aws_api_gateway_method.op_get_metrics.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.op_get_metrics.invoke_arn
}

# =============================================================================
# /logs メソッド
# =============================================================================

# GET /logs — CloudWatch ログ取得
resource "aws_api_gateway_method" "op_get_logs" {
  rest_api_id   = aws_api_gateway_rest_api.op.id
  resource_id   = aws_api_gateway_resource.op_logs.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "op_get_logs" {
  rest_api_id             = aws_api_gateway_rest_api.op.id
  resource_id             = aws_api_gateway_resource.op_logs.id
  http_method             = aws_api_gateway_method.op_get_logs.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.op_get_logs.invoke_arn
}

# =============================================================================
# CORS 設定 — OPTIONS メソッド
# =============================================================================

# OPTIONS /metrics
resource "aws_api_gateway_method" "op_options_metrics" {
  rest_api_id   = aws_api_gateway_rest_api.op.id
  resource_id   = aws_api_gateway_resource.op_metrics.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "op_options_metrics" {
  rest_api_id = aws_api_gateway_rest_api.op.id
  resource_id = aws_api_gateway_resource.op_metrics.id
  http_method = aws_api_gateway_method.op_options_metrics.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "op_options_metrics_200" {
  rest_api_id = aws_api_gateway_rest_api.op.id
  resource_id = aws_api_gateway_resource.op_metrics.id
  http_method = aws_api_gateway_method.op_options_metrics.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }

  response_models = {
    "application/json" = "Empty"
  }
}

resource "aws_api_gateway_integration_response" "op_options_metrics" {
  rest_api_id = aws_api_gateway_rest_api.op.id
  resource_id = aws_api_gateway_resource.op_metrics.id
  http_method = aws_api_gateway_method.op_options_metrics.http_method
  status_code = aws_api_gateway_method_response.op_options_metrics_200.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

# OPTIONS /logs
resource "aws_api_gateway_method" "op_options_logs" {
  rest_api_id   = aws_api_gateway_rest_api.op.id
  resource_id   = aws_api_gateway_resource.op_logs.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "op_options_logs" {
  rest_api_id = aws_api_gateway_rest_api.op.id
  resource_id = aws_api_gateway_resource.op_logs.id
  http_method = aws_api_gateway_method.op_options_logs.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "op_options_logs_200" {
  rest_api_id = aws_api_gateway_rest_api.op.id
  resource_id = aws_api_gateway_resource.op_logs.id
  http_method = aws_api_gateway_method.op_options_logs.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }

  response_models = {
    "application/json" = "Empty"
  }
}

resource "aws_api_gateway_integration_response" "op_options_logs" {
  rest_api_id = aws_api_gateway_rest_api.op.id
  resource_id = aws_api_gateway_resource.op_logs.id
  http_method = aws_api_gateway_method.op_options_logs.http_method
  status_code = aws_api_gateway_method_response.op_options_logs_200.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}
