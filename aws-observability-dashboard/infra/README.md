# インフラストラクチャ（Terraform）

AWS サーバーレスアプリケーション「serverless-insight」のインフラストラクチャ定義です。

## ディレクトリ構成

```
infra/
├── main.tf              # Terraform / Provider 設定
├── variables.tf         # 共通変数定義
├── outputs.tf           # 出力定義
├── dynamodb.tf          # DynamoDB テーブル（posts）
├── api_gateway.tf       # API Gateway REST API（Demo App）
├── api_gateway_op.tf    # API Gateway REST API（Observability Platform）
├── iam.tf               # IAM ロール・ポリシー（Demo App Lambda）
├── iam_op.tf            # IAM ロール・ポリシー（OP Lambda）
└── README.md            # 本ドキュメント
```

## 前提条件

- Terraform >= 0.13
- AWS CLI が設定済み（認証情報・リージョン）
- 対象リージョン: `ap-northeast-1`

## リソース一覧

### DynamoDB

| リソース | 説明 |
|----------|------|
| `aws_dynamodb_table.posts` | Demo App 投稿データテーブル（オンデマンドキャパシティ） |

**テーブル設計:**

| 属性 | 型 | 説明 |
|------|----|------|
| `id` | S (String) | パーティションキー |

### API Gateway

| リソース | パス | メソッド |
|----------|------|----------|
| Demo App REST API | `/posts` | GET, POST, OPTIONS |
|                    | `/posts/{id}` | GET, DELETE, OPTIONS |
| OP REST API | `/metrics` | GET, OPTIONS |
|             | `/logs` | GET, OPTIONS |

- エンドポイントタイプ: REGIONAL
- CORS: 全オリジン許可（開発向け設定）
- Lambda プロキシ統合は後日 Lambda 関数作成時に追加
- OP API は Demo App とは独立した REST API

### IAM

| リソース | 説明 |
|----------|------|
| `aws_iam_role.demo_lambda_role` | Demo App Lambda 実行ロール |
| `aws_iam_policy.demo_lambda_logs` | CloudWatch Logs 書き込みポリシー |
| `aws_iam_policy.demo_lambda_dynamodb` | DynamoDB CRUD ポリシー（posts テーブル限定） |
| `aws_iam_role.op_lambda_role` | OP Lambda 実行ロール |
| `aws_iam_policy.op_lambda_logs_write` | OP Lambda — CloudWatch Logs 書き込み権限 |
| `aws_iam_policy.op_lambda_cloudwatch_metrics_read` | OP Lambda — CloudWatch Metrics 読み取り権限 |
| `aws_iam_policy.op_lambda_cloudwatch_logs_read` | OP Lambda — CloudWatch Logs 読み取り権限 |

**最小権限の原則:**
- Demo App:
  - CloudWatch Logs: `CreateLogGroup`, `CreateLogStream`, `PutLogEvents`（ログ書き込みのみ）
  - DynamoDB: `GetItem`, `PutItem`, `DeleteItem`, `Scan`（posts テーブルのみ）
- OP:
  - CloudWatch Logs 書き込み: `CreateLogGroup`, `CreateLogStream`, `PutLogEvents`（OP Lambda 自身のログ出力用、`/aws/lambda/${project_name}-op-*` に限定）
  - CloudWatch Metrics 読み取り: `GetMetricData`, `ListMetrics`
  - CloudWatch Logs 読み取り: `StartQuery`, `GetQueryResults`, `DescribeLogGroups`, `FilterLogEvents`

## 変数一覧

| 変数名 | デフォルト値 | 説明 |
|--------|-------------|------|
| `aws_region` | `ap-northeast-1` | AWS リージョン |
| `project_name` | `serverless-insight` | プロジェクト名 |
| `environment` | `production` | デプロイ環境 |
| `dynamodb_table_name` | `posts` | DynamoDB テーブル名 |
| `demo_api_name` | `demo-app-api` | Demo App REST API 名 |
| `demo_api_description` | `Demo App REST API for serverless-insight` | REST API 説明 |
| `demo_api_stage_name` | `v1` | API ステージ名 |
| `op_api_name` | `op-api` | OP REST API 名 |
| `op_api_description` | `Observability Platform REST API for serverless-insight` | OP REST API 説明 |
| `op_api_stage_name` | `v1` | OP API ステージ名 |
| `op_metrics_lambda_arn` | `arn:aws:lambda:ap-northeast-1:000000000000:function:placeholder-metrics` | OP メトリクス取得 Lambda ARN（後日設定） |
| `op_logs_lambda_arn` | `arn:aws:lambda:ap-northeast-1:000000000000:function:placeholder-logs` | OP ログ取得 Lambda ARN（後日設定） |

## 使用方法

### 初期化

```bash
cd aws-observability-dashboard/infra
terraform init
```

### プラン確認

```bash
terraform plan
```

### デプロイ

```bash
terraform apply
```

### 変数の上書き

```bash
terraform plan -var="environment=staging" -var="dynamodb_table_name=posts-staging"
```

## タグ付け規則

全リソースに以下のデフォルトタグが付与されます:

| タグキー | 値 |
|----------|-----|
| `Project` | `serverless-insight` |
| `Environment` | `production` |
| `ManagedBy` | `terraform` |

## 今後の追加予定

- Lambda 関数定義（PBI-002, PBI-003, PBI-004, PBI-005）
- API Gateway と Lambda のプロキシ統合
- API Gateway デプロイ・ステージ設定
- ~~Observability Platform 用リソース（PBI-010）~~ ✅ 完了
- OP Lambda 関数定義（PBI-011, PBI-012）
- OP API Gateway デプロイ・ステージ設定
- `op_metrics_lambda_arn` / `op_logs_lambda_arn` の実値設定
