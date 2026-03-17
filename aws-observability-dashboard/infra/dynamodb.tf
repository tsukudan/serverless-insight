###############################################################################
# DynamoDB テーブル定義 — Demo App (posts)
###############################################################################

resource "aws_dynamodb_table" "posts" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST" # オンデマンドキャパシティ（低コスト向け）

  hash_key = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name = var.dynamodb_table_name
  }
}
