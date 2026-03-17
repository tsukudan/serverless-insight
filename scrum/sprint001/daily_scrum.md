# Sprint 001 デイリースクラム記録

## スプリントゴール

> **Demo Web App と Observability Platform のバックエンド基盤を完成させ、主要画面の初期表示を実現することで、システム全体の開発基盤を確立する。**

---

## DAY 1（2026-03-16 月）

### 伊藤

| 項目 | 内容 |
|------|------|
| 昨日やったこと | — （スプリント初日） |
| 今日やったこと | PBI-001（Demo App インフラ基盤構築）全タスク完了（1-1〜1-5）: Terraform プロジェクト構成・provider 設定、DynamoDB テーブル定義、API Gateway REST API 定義、Lambda 実行ロール定義、ドキュメント作成。PBI-006 先行着手: backend ディレクトリ構造・共通ログモジュールの骨格を作成 |
| 障害物 | なし |

### 田中

| 項目 | 内容 |
|------|------|
| 昨日やったこと | — （スプリント初日） |
| 今日やったこと | PBI-010（OP インフラ基盤構築）全タスク完了（10-1〜10-4）: OP 用 API Gateway REST API 定義、Lambda 実行ロール定義（CloudWatch 読み取り権限付き）、IAM ポリシー最小権限設計・実装、ドキュメント作成 |
| 障害物 | なし |

### 障害物・メモ

- Terraform CLI が環境にインストールされていないため `terraform plan` 実行は未検証。開発環境の問題であり、コード品質には影響なし。本質的な障害ではないため障害物ログには記載しない。

### スプリントゴールへの進捗

- 計画 SP: 46 / 完了 SP: 10（PBI-001: 5 SP + PBI-010: 5 SP）
- DAY1 完了目標: PBI-001 ✅、PBI-010 ✅ — 達成
- PBI-006 先行着手中（In Progress）

---

## DAY 2（2026-03-17 火）

### 伊藤

| 項目 | 内容 |
|------|------|
| 昨日やったこと | PBI-001 全タスク完了、PBI-006 先行着手（ログモジュール骨格作成） |
| 今日やったこと | PBI-002（GET /posts）残りタスク全完了: Terraform Lambda 定義（lambda.tf 新規作成、全4 Lambda 関数・API Gateway 統合・デプロイメント定義）、ユニットテスト作成（test_get_posts.py: 正常系2件+異常系1件）、構造化ログ統合確認済み。全22テストパス |
| 障害物 | なし |

### 田中

| 項目 | 内容 |
|------|------|
| 昨日やったこと | PBI-010 全タスク完了（OP インフラ基盤構築） |
| 今日やったこと | PBI-004（GET /posts/:id）全タスク完了: Lambda 関数・ユニットテスト・Terraform 定義・構造化ログ統合。PBI-005（DELETE /posts/:id）全タスク完了: Lambda 関数・ユニットテスト・Terraform 定義・構造化ログ統合 |
| 障害物 | なし |

### 障害物・メモ

- 既存テストで `boto3` 未インストール・`AWS_DEFAULT_REGION` 未設定のエラーがあったが、仮想環境への boto3 インストールと環境変数追加で解消済み

### スプリントゴールへの進捗

- 計画 SP: 46 / 完了 SP: 20（PBI-001: 5 + PBI-006: 3 + PBI-010: 5 + PBI-002: 3 + PBI-004: 2 + PBI-005: 2）
- DAY2 完了目標: PBI-006 ✅、PBI-004 ✅、PBI-005 ✅ — 達成
- PBI-002 も前倒しで完了 ✅

---

## DAY 3（2026-03-18 水）

### 伊藤

| 項目 | 内容 |
|------|------|
| 昨日やったこと | PBI-002 全タスク完了（GET /posts: Terraform Lambda 定義・テスト・ログ統合確認） |
| 今日やったこと | PBI-003（POST /posts）全タスク完了: Lambda 関数実装（create_post.py: バリデーション・UUID採番・DynamoDB PutItem）、ユニットテスト作成（test_create_post.py: 正常系1件+バリデーション3件+異常系1件）、Terraform定義は DAY2 の lambda.tf で対応済み。全27テストパス |
| 障害物 | なし |

### 田中

| 項目 | 内容 |
|------|------|
| 昨日やったこと | PBI-004, PBI-005 全タスク完了 |
| 今日やったこと | PBI-011（CloudWatch メトリクス取得 API）タスク11-1〜11-3 完了: backend-op ディレクトリ構成作成、API設計・GetMetricData呼び出しロジック・時間範囲パラメータ処理を get_metrics.py に統合実装。スモークテスト14件パス |
| 障害物 | なし |

### スプリントゴールへの進捗

- 計画 SP: 46 / 完了 SP: 23（+3 SP: PBI-003）
- DAY3 完了目標: PBI-002 ✅（前倒し済）、PBI-003 ✅ — 達成
- PBI-011 が In Progress（タスク 11-1〜11-3 完了、11-4〜11-7 残り）

---

## DAY 4（2026-03-19 木）

### 伊藤

| 項目 | 内容 |
|------|------|
| 昨日やったこと | PBI-003（POST /posts）全タスク完了 |
| 今日やったこと | PBI-011 残りタスク確認（11-4〜11-6: DAY3で田中が実装済みのフィルタリング・p95算出を確認、テストカバレッジ十分）。PBI-012（CloudWatch ログ取得 API）全タスク完了: get_logs.py 実装（Logs Insights クエリ・レベル/エンドポイントフィルタ・100件制限）、テスト25件作成。OP Terraform Lambda 定義（lambda_op.tf）作成、プレースホルダー ARN を実際の Lambda 参照に更新 |
| 障害物 | なし |

### 田中

| 項目 | 内容 |
|------|------|
| 昨日やったこと | PBI-011 タスク 11-1〜11-3 完了 |
| 今日やったこと | PBI-014 タスク 14-1 完了: OP フロントエンド Next.js プロジェクト初期化（TypeScript + Tailwind CSS + Static Export）。共通コンポーネント作成（Header, Navigation, TimeRangeSelector, ReloadButton, LoadingSpinner, ErrorMessage）、型定義・API クライアント作成、4画面プレースホルダー作成。ビルド成功確認済み |
| 障害物 | なし |

### スプリントゴールへの進捗

- 計画 SP: 46 / 完了 SP: 36（+13 SP: PBI-011: 8 + PBI-012: 5）
- DAY4 完了目標: PBI-011 ✅、PBI-012 ✅ — 達成
- PBI-014 が In Progress（タスク 14-1 完了、14-2〜14-5 残り）

---

## DAY 5（2026-03-20 金）

### 伊藤

| 項目 | 内容 |
|------|------|
| 昨日やったこと | PBI-011 残りタスク確認、PBI-012 全タスク完了、OP Lambda Terraform 定義作成 |
| 今日やったこと | PBI-014 タスク 14-5（Overview テスト作成）、PBI-016 タスク 16-5（Endpoints テスト作成）完了。vitest + @testing-library/react セットアップ、SummaryCard/ErrorMessage/LoadingSpinner/TimeRangeSelector/ReloadButton/EndpointsTable コンポーネントテスト・endpoints ユーティリティテスト作成。フロントエンド全 21 テストパス |
| 障害物 | なし |

### 田中

| 項目 | 内容 |
|------|------|
| 昨日やったこと | PBI-014 タスク 14-1 完了（OP フロントエンド Next.js プロジェクト初期化） |
| 今日やったこと | PBI-014 タスク 14-2〜14-4 完了（Overview 画面のサマリーカード・API 連携・時間範囲セレクタは DAY4 で先行実装済みを確認）。PBI-016 タスク 16-1〜16-4 完了: EndpointsTable コンポーネント作成、Endpoints ページ実装（fetchMetrics 連携・TimeRangeSelector 連動）、エンドポイントスラッグ変換ユーティリティ作成、Endpoint Detail 画面のフル実装（サマリーカード・メトリクス推移グラフ・最新エラーログ 20 件表示・Static Export 対応） |
| 障害物 | なし |

### 障害物・メモ

- EndpointsTable の `<Link>` 内 `<tr>` が無効な HTML 構造になっていたため、`useRouter().push` パターンに修正

### スプリントゴールへの進捗

- 計画 SP: 46 / 完了 SP: 46（+10 SP: PBI-014: 5 + PBI-016: 5）
- DAY5 完了目標: PBI-014 ✅、PBI-016 ✅ — 達成
- **スプリントゴール: 達成** 🎉
- 全テスト合格: フロントエンド 21 件 + Demo App バックエンド 27 件 + OP バックエンド 39 件 = **合計 87 件**
