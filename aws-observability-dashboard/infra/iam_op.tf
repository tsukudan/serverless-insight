###############################################################################
# IAM ロール・ポリシー定義 — Observability Platform (OP) Lambda
###############################################################################

# -----------------------------------------------------------------------------
# Lambda 実行ロール
# -----------------------------------------------------------------------------

resource "aws_iam_role" "op_lambda_role" {
  name               = "${var.project_name}-op-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = {
    Name = "${var.project_name}-op-lambda-role"
  }
}

# -----------------------------------------------------------------------------
# CloudWatch Logs 書き込みポリシー（OP Lambda 自身のログ出力用）
# -----------------------------------------------------------------------------

data "aws_iam_policy_document" "op_lambda_logs_write" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:${var.aws_region}:*:log-group:/aws/lambda/${var.project_name}-op-*:*"]
  }
}

resource "aws_iam_policy" "op_lambda_logs_write" {
  name        = "${var.project_name}-op-lambda-logs-write"
  description = "OP Lambda — CloudWatch Logs 書き込み権限（自身のログ出力用）"
  policy      = data.aws_iam_policy_document.op_lambda_logs_write.json
}

resource "aws_iam_role_policy_attachment" "op_lambda_logs_write" {
  role       = aws_iam_role.op_lambda_role.name
  policy_arn = aws_iam_policy.op_lambda_logs_write.arn
}

# -----------------------------------------------------------------------------
# CloudWatch Metrics 読み取りポリシー（最小権限）
# -----------------------------------------------------------------------------

data "aws_iam_policy_document" "op_lambda_cloudwatch_metrics_read" {
  statement {
    effect = "Allow"
    actions = [
      "cloudwatch:GetMetricData",
      "cloudwatch:ListMetrics",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "op_lambda_cloudwatch_metrics_read" {
  name        = "${var.project_name}-op-lambda-cw-metrics-read"
  description = "OP Lambda — CloudWatch Metrics 読み取り権限"
  policy      = data.aws_iam_policy_document.op_lambda_cloudwatch_metrics_read.json
}

resource "aws_iam_role_policy_attachment" "op_lambda_cloudwatch_metrics_read" {
  role       = aws_iam_role.op_lambda_role.name
  policy_arn = aws_iam_policy.op_lambda_cloudwatch_metrics_read.arn
}

# -----------------------------------------------------------------------------
# CloudWatch Logs 読み取りポリシー（最小権限）
# -----------------------------------------------------------------------------

data "aws_iam_policy_document" "op_lambda_cloudwatch_logs_read" {
  statement {
    effect = "Allow"
    actions = [
      "logs:StartQuery",
      "logs:GetQueryResults",
      "logs:DescribeLogGroups",
      "logs:FilterLogEvents",
    ]
    resources = ["arn:aws:logs:${var.aws_region}:*:log-group:*"]
  }
}

resource "aws_iam_policy" "op_lambda_cloudwatch_logs_read" {
  name        = "${var.project_name}-op-lambda-cw-logs-read"
  description = "OP Lambda — CloudWatch Logs 読み取り権限"
  policy      = data.aws_iam_policy_document.op_lambda_cloudwatch_logs_read.json
}

resource "aws_iam_role_policy_attachment" "op_lambda_cloudwatch_logs_read" {
  role       = aws_iam_role.op_lambda_role.name
  policy_arn = aws_iam_policy.op_lambda_cloudwatch_logs_read.arn
}
