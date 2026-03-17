###############################################################################
# Lambda 関数定義 — Demo App
###############################################################################

# =============================================================================
# デプロイパッケージ（ZIP アーカイブ）
# =============================================================================

data "archive_file" "demo_backend" {
  type        = "zip"
  source_dir  = "${path.module}/../app/backend"
  output_path = "${path.module}/../app/backend/deploy.zip"
  excludes    = ["tests", "__pycache__", "deploy.zip", ".pytest_cache"]
}

# =============================================================================
# Lambda 関数
# =============================================================================

# --- GET /posts — 投稿一覧取得 -----------------------------------------------
resource "aws_lambda_function" "get_posts" {
  function_name    = "${var.project_name}-demo-get_posts"
  runtime          = "python3.12"
  handler          = "handlers/get_posts.lambda_handler"
  role             = aws_iam_role.demo_lambda_role.arn
  filename         = data.archive_file.demo_backend.output_path
  source_code_hash = data.archive_file.demo_backend.output_base64sha256
  timeout          = 10

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }

  tags = {
    Name = "${var.project_name}-demo-get_posts"
  }
}

# --- GET /posts/{id} — 投稿詳細取得 ------------------------------------------
resource "aws_lambda_function" "get_post" {
  function_name    = "${var.project_name}-demo-get_post"
  runtime          = "python3.12"
  handler          = "handlers/get_post.lambda_handler"
  role             = aws_iam_role.demo_lambda_role.arn
  filename         = data.archive_file.demo_backend.output_path
  source_code_hash = data.archive_file.demo_backend.output_base64sha256
  timeout          = 10

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }

  tags = {
    Name = "${var.project_name}-demo-get_post"
  }
}

# --- DELETE /posts/{id} — 投稿削除 -------------------------------------------
resource "aws_lambda_function" "delete_post" {
  function_name    = "${var.project_name}-demo-delete_post"
  runtime          = "python3.12"
  handler          = "handlers/delete_post.lambda_handler"
  role             = aws_iam_role.demo_lambda_role.arn
  filename         = data.archive_file.demo_backend.output_path
  source_code_hash = data.archive_file.demo_backend.output_base64sha256
  timeout          = 10

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }

  tags = {
    Name = "${var.project_name}-demo-delete_post"
  }
}

# --- POST /posts — 投稿作成（DAY3 でハンドラ実装予定） -----------------------
resource "aws_lambda_function" "create_post" {
  function_name    = "${var.project_name}-demo-create_post"
  runtime          = "python3.12"
  handler          = "handlers/create_post.lambda_handler"
  role             = aws_iam_role.demo_lambda_role.arn
  filename         = data.archive_file.demo_backend.output_path
  source_code_hash = data.archive_file.demo_backend.output_base64sha256
  timeout          = 10

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }

  tags = {
    Name = "${var.project_name}-demo-create_post"
  }
}

# =============================================================================
# API Gateway — Lambda プロキシ統合（AWS_PROXY）
# =============================================================================

# --- GET /posts ---------------------------------------------------------------
resource "aws_api_gateway_integration" "get_posts" {
  rest_api_id             = aws_api_gateway_rest_api.demo_app.id
  resource_id             = aws_api_gateway_resource.posts.id
  http_method             = aws_api_gateway_method.get_posts.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.get_posts.invoke_arn
}

# --- POST /posts --------------------------------------------------------------
resource "aws_api_gateway_integration" "post_posts" {
  rest_api_id             = aws_api_gateway_rest_api.demo_app.id
  resource_id             = aws_api_gateway_resource.posts.id
  http_method             = aws_api_gateway_method.post_posts.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.create_post.invoke_arn
}

# --- GET /posts/{id} ----------------------------------------------------------
resource "aws_api_gateway_integration" "get_posts_id" {
  rest_api_id             = aws_api_gateway_rest_api.demo_app.id
  resource_id             = aws_api_gateway_resource.posts_id.id
  http_method             = aws_api_gateway_method.get_posts_id.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.get_post.invoke_arn
}

# --- DELETE /posts/{id} -------------------------------------------------------
resource "aws_api_gateway_integration" "delete_posts_id" {
  rest_api_id             = aws_api_gateway_rest_api.demo_app.id
  resource_id             = aws_api_gateway_resource.posts_id.id
  http_method             = aws_api_gateway_method.delete_posts_id.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.delete_post.invoke_arn
}

# =============================================================================
# Lambda 実行権限（API Gateway → Lambda）
# =============================================================================

resource "aws_lambda_permission" "get_posts" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_posts.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.demo_app.execution_arn}/*/GET/posts"
}

resource "aws_lambda_permission" "create_post" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_post.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.demo_app.execution_arn}/*/POST/posts"
}

resource "aws_lambda_permission" "get_post" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_post.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.demo_app.execution_arn}/*/GET/posts/*"
}

resource "aws_lambda_permission" "delete_post" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.delete_post.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.demo_app.execution_arn}/*/DELETE/posts/*"
}

# =============================================================================
# API Gateway デプロイメント & ステージ
# =============================================================================

resource "aws_api_gateway_deployment" "demo_app" {
  rest_api_id = aws_api_gateway_rest_api.demo_app.id

  depends_on = [
    aws_api_gateway_integration.get_posts,
    aws_api_gateway_integration.post_posts,
    aws_api_gateway_integration.get_posts_id,
    aws_api_gateway_integration.delete_posts_id,
    aws_api_gateway_integration.options_posts,
    aws_api_gateway_integration.options_posts_id,
  ]

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.posts,
      aws_api_gateway_resource.posts_id,
      aws_api_gateway_method.get_posts,
      aws_api_gateway_method.post_posts,
      aws_api_gateway_method.get_posts_id,
      aws_api_gateway_method.delete_posts_id,
      aws_api_gateway_integration.get_posts,
      aws_api_gateway_integration.post_posts,
      aws_api_gateway_integration.get_posts_id,
      aws_api_gateway_integration.delete_posts_id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "demo_app" {
  deployment_id = aws_api_gateway_deployment.demo_app.id
  rest_api_id   = aws_api_gateway_rest_api.demo_app.id
  stage_name    = var.demo_api_stage_name

  tags = {
    Name = "${var.project_name}-demo-${var.demo_api_stage_name}"
  }
}
