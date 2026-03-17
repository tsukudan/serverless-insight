###############################################################################
# API Gateway REST API 定義 — Demo App
###############################################################################

resource "aws_api_gateway_rest_api" "demo_app" {
  name        = var.demo_api_name
  description = var.demo_api_description

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# =============================================================================
# リソース定義
# =============================================================================

# /posts
resource "aws_api_gateway_resource" "posts" {
  rest_api_id = aws_api_gateway_rest_api.demo_app.id
  parent_id   = aws_api_gateway_rest_api.demo_app.root_resource_id
  path_part   = "posts"
}

# /posts/{id}
resource "aws_api_gateway_resource" "posts_id" {
  rest_api_id = aws_api_gateway_rest_api.demo_app.id
  parent_id   = aws_api_gateway_resource.posts.id
  path_part   = "{id}"
}

# =============================================================================
# /posts メソッド
# =============================================================================

# GET /posts — 投稿一覧取得
resource "aws_api_gateway_method" "get_posts" {
  rest_api_id   = aws_api_gateway_rest_api.demo_app.id
  resource_id   = aws_api_gateway_resource.posts.id
  http_method   = "GET"
  authorization = "NONE"
}

# POST /posts — 投稿作成
resource "aws_api_gateway_method" "post_posts" {
  rest_api_id   = aws_api_gateway_rest_api.demo_app.id
  resource_id   = aws_api_gateway_resource.posts.id
  http_method   = "POST"
  authorization = "NONE"
}

# =============================================================================
# /posts/{id} メソッド
# =============================================================================

# GET /posts/{id} — 投稿詳細取得
resource "aws_api_gateway_method" "get_posts_id" {
  rest_api_id   = aws_api_gateway_rest_api.demo_app.id
  resource_id   = aws_api_gateway_resource.posts_id.id
  http_method   = "GET"
  authorization = "NONE"
}

# DELETE /posts/{id} — 投稿削除
resource "aws_api_gateway_method" "delete_posts_id" {
  rest_api_id   = aws_api_gateway_rest_api.demo_app.id
  resource_id   = aws_api_gateway_resource.posts_id.id
  http_method   = "DELETE"
  authorization = "NONE"
}

# =============================================================================
# CORS 設定 — OPTIONS メソッド
# =============================================================================

# OPTIONS /posts
resource "aws_api_gateway_method" "options_posts" {
  rest_api_id   = aws_api_gateway_rest_api.demo_app.id
  resource_id   = aws_api_gateway_resource.posts.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "options_posts" {
  rest_api_id = aws_api_gateway_rest_api.demo_app.id
  resource_id = aws_api_gateway_resource.posts.id
  http_method = aws_api_gateway_method.options_posts.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "options_posts_200" {
  rest_api_id = aws_api_gateway_rest_api.demo_app.id
  resource_id = aws_api_gateway_resource.posts.id
  http_method = aws_api_gateway_method.options_posts.http_method
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

resource "aws_api_gateway_integration_response" "options_posts" {
  rest_api_id = aws_api_gateway_rest_api.demo_app.id
  resource_id = aws_api_gateway_resource.posts.id
  http_method = aws_api_gateway_method.options_posts.http_method
  status_code = aws_api_gateway_method_response.options_posts_200.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

# OPTIONS /posts/{id}
resource "aws_api_gateway_method" "options_posts_id" {
  rest_api_id   = aws_api_gateway_rest_api.demo_app.id
  resource_id   = aws_api_gateway_resource.posts_id.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "options_posts_id" {
  rest_api_id = aws_api_gateway_rest_api.demo_app.id
  resource_id = aws_api_gateway_resource.posts_id.id
  http_method = aws_api_gateway_method.options_posts_id.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "options_posts_id_200" {
  rest_api_id = aws_api_gateway_rest_api.demo_app.id
  resource_id = aws_api_gateway_resource.posts_id.id
  http_method = aws_api_gateway_method.options_posts_id.http_method
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

resource "aws_api_gateway_integration_response" "options_posts_id" {
  rest_api_id = aws_api_gateway_rest_api.demo_app.id
  resource_id = aws_api_gateway_resource.posts_id.id
  http_method = aws_api_gateway_method.options_posts_id.http_method
  status_code = aws_api_gateway_method_response.options_posts_id_200.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,DELETE,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}
