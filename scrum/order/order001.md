# 依頼事項メモ — order001

> **作成日:** 2026-03-16
> **依頼者:** 上長
> **ステータス:** 新規

---

## 依頼概要

`docs/RD/requirements.md` に記載された要件定義書に基づき、Serverless Insight（AWS サーバーレスアプリ向けオブザーバビリティプラットフォーム）の MVP を開発すること。

## 対象システム

### 1. Demo Web App（監視対象アプリ）

シンプルな投稿 CRUD アプリケーション。Observability Platform の監視対象として動作する。

- **API エンドポイント:**
  - `GET /posts` — 投稿一覧を取得
  - `POST /posts` — 新規投稿を作成
  - `GET /posts/:id` — 特定の投稿を取得
  - `DELETE /posts/:id` — 特定の投稿を削除

- **データモデル:** Post（id, title, body, createdAt, updatedAt）
- **アーキテクチャ:** CloudFront → S3 (Next.js Static Export) → API Gateway → Lambda (Python) → DynamoDB
- **構造化ログ:** 全 Lambda 関数で JSON 形式の構造化ログを出力

### 2. Observability Platform（監視ダッシュボード）

CloudWatch からメトリクス・ログを取得してダッシュボード表示する監視ツール。

- **画面構成:**
  - Overview — アプリ全体の健康状態（総リクエスト数、エラー率、平均レスポンス時間、p95レイテンシ、推移グラフ）
  - Endpoints — API エンドポイント一覧の運用状況
  - Endpoint Detail — 特定 API の詳細なメトリクス・ログ
  - Logs — ログビューア（レベルフィルタ、エンドポイントフィルタ）

- **共通機能:** 時間範囲セレクタ（1h/6h/24h/7d）、手動リロード、エラー表示、ローディング表示
- **アーキテクチャ:** CloudFront → Next.js (Static Export) → API Gateway → Lambda (Python) → CloudWatch API

## 技術スタック

| レイヤー | 技術 |
|---------|------|
| Frontend | Next.js (Static Export), TypeScript, Tailwind CSS |
| Backend | AWS Lambda (Python), API Gateway |
| Data Source | CloudWatch Metrics, CloudWatch Logs |
| Database | DynamoDB（Demo App 用） |
| Hosting | CloudFront + S3 |
| IaC | Terraform |

## 主要な非機能要件

- ダッシュボード初期表示: 3秒以内
- APIレスポンス時間: 5秒以内
- 月額コスト: $1以下
- リージョン: ap-northeast-1（東京）のみ
- IAM 最小権限の原則
- 全インフラを Terraform で管理

## 顧客としての期待

- アプリケーション全体の健康状態が一目でわかること
- APIエンドポイント単位のパフォーマンスが確認できること
- エラーログを迅速に確認・調査できること
- シンプルで使いやすいUIであること

---

> **備考:** 要件定義書の詳細は `docs/RD/requirements.md` を参照のこと。

---

## 対応状況

- [x] 2026-03-16: プロダクトバックログに全要件が取り込まれた（PBI-001〜PBI-022、合計93SP）
- [x] 2026-03-16: プロダクトゴール、完成の定義が策定された
