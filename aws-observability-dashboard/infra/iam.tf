###############################################################################
# IAM ロール・ポリシー定義 — Demo App Lambda
###############################################################################

# -----------------------------------------------------------------------------
# Lambda 実行ロール
# -----------------------------------------------------------------------------

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "demo_lambda_role" {
  name               = "${var.project_name}-demo-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = {
    Name = "${var.project_name}-demo-lambda-role"
  }
}

# -----------------------------------------------------------------------------
# CloudWatch Logs ポリシー（最小権限）
# -----------------------------------------------------------------------------

data "aws_iam_policy_document" "demo_lambda_logs" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:${var.aws_region}:*:log-group:/aws/lambda/${var.project_name}-demo-*:*"]
  }
}

resource "aws_iam_policy" "demo_lambda_logs" {
  name        = "${var.project_name}-demo-lambda-logs"
  description = "Demo App Lambda — CloudWatch Logs 書き込み権限"
  policy      = data.aws_iam_policy_document.demo_lambda_logs.json
}

resource "aws_iam_role_policy_attachment" "demo_lambda_logs" {
  role       = aws_iam_role.demo_lambda_role.name
  policy_arn = aws_iam_policy.demo_lambda_logs.arn
}

# -----------------------------------------------------------------------------
# DynamoDB CRUD ポリシー（最小権限）
# -----------------------------------------------------------------------------

data "aws_iam_policy_document" "demo_lambda_dynamodb" {
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:DeleteItem",
      "dynamodb:Scan",
    ]
    resources = [aws_dynamodb_table.posts.arn]
  }
}

resource "aws_iam_policy" "demo_lambda_dynamodb" {
  name        = "${var.project_name}-demo-lambda-dynamodb"
  description = "Demo App Lambda — DynamoDB CRUD 権限（posts テーブル）"
  policy      = data.aws_iam_policy_document.demo_lambda_dynamodb.json
}

resource "aws_iam_role_policy_attachment" "demo_lambda_dynamodb" {
  role       = aws_iam_role.demo_lambda_role.name
  policy_arn = aws_iam_policy.demo_lambda_dynamodb.arn
}
