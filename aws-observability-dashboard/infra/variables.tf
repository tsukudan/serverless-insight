###############################################################################
# 共通変数定義
###############################################################################

variable "aws_region" {
  description = "AWS リージョン"
  type        = string
  default     = "ap-northeast-1"
}

variable "project_name" {
  description = "プロジェクト名（タグ付けに使用）"
  type        = string
  default     = "serverless-insight"
}

variable "environment" {
  description = "デプロイ環境"
  type        = string
  default     = "production"
}

# -----------------------------------------------------------------------------
# DynamoDB
# -----------------------------------------------------------------------------

variable "dynamodb_table_name" {
  description = "Demo App 用 DynamoDB テーブル名"
  type        = string
  default     = "posts"
}

# -----------------------------------------------------------------------------
# API Gateway
# -----------------------------------------------------------------------------

variable "demo_api_name" {
  description = "Demo App 用 REST API 名"
  type        = string
  default     = "demo-app-api"
}

variable "demo_api_description" {
  description = "Demo App 用 REST API の説明"
  type        = string
  default     = "Demo App REST API for serverless-insight"
}

variable "demo_api_stage_name" {
  description = "Demo App API のデプロイステージ名"
  type        = string
  default     = "v1"
}

# -----------------------------------------------------------------------------
# Observability Platform (OP) API Gateway
# -----------------------------------------------------------------------------

variable "op_api_name" {
  description = "OP 用 REST API 名"
  type        = string
  default     = "op-api"
}

variable "op_api_description" {
  description = "OP 用 REST API の説明"
  type        = string
  default     = "Observability Platform REST API for serverless-insight"
}

variable "op_api_stage_name" {
  description = "OP API のデプロイステージ名"
  type        = string
  default     = "v1"
}


