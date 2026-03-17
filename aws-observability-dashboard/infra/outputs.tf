###############################################################################
# 出力定義
###############################################################################

# -----------------------------------------------------------------------------
# DynamoDB
# -----------------------------------------------------------------------------

output "dynamodb_table_name" {
  description = "DynamoDB テーブル名"
  value       = aws_dynamodb_table.posts.name
}

output "dynamodb_table_arn" {
  description = "DynamoDB テーブル ARN"
  value       = aws_dynamodb_table.posts.arn
}

# -----------------------------------------------------------------------------
# API Gateway
# -----------------------------------------------------------------------------

output "demo_api_id" {
  description = "Demo App REST API ID"
  value       = aws_api_gateway_rest_api.demo_app.id
}

output "demo_api_root_resource_id" {
  description = "Demo App REST API ルートリソース ID"
  value       = aws_api_gateway_rest_api.demo_app.root_resource_id
}

output "demo_api_execution_arn" {
  description = "Demo App REST API 実行 ARN"
  value       = aws_api_gateway_rest_api.demo_app.execution_arn
}

# -----------------------------------------------------------------------------
# IAM
# -----------------------------------------------------------------------------

output "demo_lambda_role_arn" {
  description = "Demo App Lambda 実行ロール ARN"
  value       = aws_iam_role.demo_lambda_role.arn
}

output "demo_lambda_role_name" {
  description = "Demo App Lambda 実行ロール名"
  value       = aws_iam_role.demo_lambda_role.name
}

# -----------------------------------------------------------------------------
# Observability Platform (OP) API Gateway
# -----------------------------------------------------------------------------

output "op_api_id" {
  description = "OP REST API ID"
  value       = aws_api_gateway_rest_api.op.id
}

output "op_api_root_resource_id" {
  description = "OP REST API ルートリソース ID"
  value       = aws_api_gateway_rest_api.op.root_resource_id
}

output "op_api_execution_arn" {
  description = "OP REST API 実行 ARN"
  value       = aws_api_gateway_rest_api.op.execution_arn
}

# -----------------------------------------------------------------------------
# Observability Platform (OP) IAM
# -----------------------------------------------------------------------------

output "op_lambda_role_arn" {
  description = "OP Lambda 実行ロール ARN"
  value       = aws_iam_role.op_lambda_role.arn
}

output "op_lambda_role_name" {
  description = "OP Lambda 実行ロール名"
  value       = aws_iam_role.op_lambda_role.name
}
