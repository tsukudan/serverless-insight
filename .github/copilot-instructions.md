# GitHub Copilot 指示書

このファイルは `serverless-insight` プロジェクトにおける GitHub Copilot のワークスペースレベルの指示を提供します。

## プロジェクト概要

`serverless-insight` は AWS サーバーレスアプリケーション向けの軽量オブザーバビリティプラットフォームです。
フロントエンド、バックエンド、およびインフラストラクチャ・アズ・コードで構成された AWS オブザーバビリティダッシュボードを提供します。

## アーキテクチャ

```
aws-observability-dashboard/
├── README.md
├── app/
│   ├── frontend/   # オブザーバビリティダッシュボードの UI
│   └── backend/    # API / サーバーレス関数
└── infra/          # Infrastructure as Code (Terraform)

scrum/                          # スクラム成果物
└── order/                      # エンドユーザサイドの要求事項や依頼事項
│   └── orderXXX.md             # 個別の要求事項ファイル（XXXは連番。常に最新のみを確認する）
├── product_goal.md             # プロダクトゴール
├── product_backlog.csv         # プロダクトバックログ（PBI一覧、CSV形式）
├── definition_of_done.md       # 完成の定義（DoD）
├── impediment_log.csv          # 障害物ログ（CSV形式）
├── velocity.csv                # ベロシティ記録（CSV形式）
└── sprintXXX/                  # スプリント別フォルダ（sprint001, sprint002, ...）
    ├── sprint_backlog.md       # スプリントバックログ（ゴール・PBI・タスク）
    ├── sprint_planning.md      # スプリントプランニング記録
    ├── sprint_review.md        # スプリントレビュー記録
    ├── sprint_retrospective.md # スプリントレトロスペクティブ記録
    └── daily_scrum.md          # デイリースクラム記録（日次追記）
```

## コーディングガイドライン

- フロントエンドおよびバックエンドのコードにはできる限り TypeScript を使用する。
- Lambda、API Gateway、DynamoDB 等のサーバーレスアーキテクチャにおける AWS ベストプラクティスに従う。
- インフラストラクチャコードは Terraformで記述する。
- イミュータブルインフラストラクチャパターンを優先する。
- すべての Lambda 関数には構造化ログ（JSON 形式）と適切なエラーハンドリングを実装する。
- 設定には環境変数を使用し、シークレットや認証情報をハードコードしない。

## テスト

- すべての Lambda 関数およびユーティリティモジュールにユニットテストを記述する。
- 非本番環境でのインフラストラクチャデプロイの検証にはインテグレーションテストを使用する。

## セキュリティ

- すべての IAM ロールおよびポリシーに最小権限の原則を適用する。
- 必要に応じて AWS CloudTrail、AWS Config、AWS Security Hub との連携を有効化する。
- デプロイ前に依存関係の既知の脆弱性をスキャンする。


## 全体ルール

- 全ての成果物は **日本語** で記述すること
- CSVファイルの列構造を変更しないこと。また文字コードはUTF-8としてExcelで文字化けしないようにする。
- スクラムガイド2020に準拠して運用すること
- nodeの場合、パッケージマネージャーはnpmを使用すること
- pythonの場合、現在の環境にある仮想環境(.venv)を使用すること
