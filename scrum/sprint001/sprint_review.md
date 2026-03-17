# Sprint 001 スプリントレビュー記録

## 実施日

2026-03-20（金）

## 参加者

| 役割 | 名前 |
|------|------|
| プロダクトオーナー | 鈴木 |
| スクラムマスター | 高橋 |
| 開発者 | 伊藤、田中 |
| ステークホルダー（顧客） | 佐藤 |

---

## 1. スプリントゴール達成状況

### スプリントゴール

> **Demo Web App と Observability Platform のバックエンド基盤を完成させ、主要画面の初期表示を実現することで、システム全体の開発基盤を確立する。**

### 結論：**達成**

| 観点 | 計画 | 実績 |
|------|------|------|
| PBI 完了数 | 11 | **11（完了率 100%）** |
| ストーリーポイント | 46 SP | **46 SP（消化率 100%）** |
| テスト | — | **87テスト全パス（FE:21 / BE:27 / OP:39）** |
| キャリーオーバー | — | **なし** |

---

## 2. インクリメントのデモと検査

### 2.1 Demo Web App バックエンド

| PBI | 成果物 | DoD 確認 |
|-----|--------|---------|
| PBI-001 | DynamoDB・API Gateway・Lambda実行ロールの Terraform 定義 | ✅ |
| PBI-002 | GET /posts Lambda（DynamoDB Scan + createdAt 降順ソート） | ✅ |
| PBI-003 | POST /posts Lambda（バリデーション + UUID採番 + DynamoDB PutItem） | ✅ |
| PBI-004 | GET /posts/:id Lambda（DynamoDB GetItem + 404ハンドリング） | ✅ |
| PBI-005 | DELETE /posts/:id Lambda（存在確認 + DynamoDB DeleteItem） | ✅ |
| PBI-006 | StructuredLogger 共通モジュール（JSON構造化ログ、INFO/WARN/ERROR） | ✅ |

### 2.2 Observability Platform バックエンド

| PBI | 成果物 | DoD 確認 |
|-----|--------|---------|
| PBI-010 | OP用 API Gateway・Lambda実行ロール（CloudWatch読み取り権限）Terraform定義 | ✅ |
| PBI-011 | CloudWatchメトリクス取得API（GetMetricData連携、時間範囲・エンドポイント別対応） | ✅ |
| PBI-012 | CloudWatchログ取得API（Logs Insights、レベル・エンドポイントフィルタ、100件制限） | ✅ |

### 2.3 Observability Platform フロントエンド

| PBI | 成果物 | DoD 確認 |
|-----|--------|---------|
| PBI-014 | Overview画面（サマリーカード4枚 + MetricsChart + TimeRangeSelector + ReloadButton） | ✅ |
| PBI-016 | Endpoints画面（EndpointsTable + 時間範囲連動 + Endpoint Detail遷移） | ✅ |

---

## 3. ステークホルダーフィードバック（佐藤）

### 3.1 機能性

- Overview画面（OP-S-01）：**要件100%充足** ✅
- Endpoints画面（OP-S-02）：**要件100%充足** ✅
- Endpoint Detail画面（OP-S-03）：OP-F-14（エラー数推移グラフ）⚠️ 、OP-F-15（ステータスコード内訳）❌
- Logs画面（OP-S-04）：フロントエンド未実装（バックエンドAPIは完成）
- 共通機能（OP-F-22〜24）：全て実装済み ✅

### 3.2 ユーザビリティ

- ローディング・エラー表示・手動リロードが全画面で統一されており良好
- Endpoints → Detail への行クリック遷移が直感的で好印象
- 時間範囲セレクタの UI が一貫している

### 3.3 ビジネス価値

- プロダクトゴールのコア価値の約70%を実現
- 「簡単に可視化」のUI動線は達成
- 「問題の迅速な特定」にはエラー推移・ステータスコード内訳・Logsが必要

### 3.4 改善提案

| # | 提案 | 優先度 |
|---|------|--------|
| 1 | Endpoint Detail にエラー数推移グラフ追加（OP-F-14） | 高 |
| 2 | Endpoint Detail にステータスコード内訳追加（OP-F-15） | 高 |
| 3 | Logs画面実装（OP-S-04） | 高 |
| 4 | MetricsChart にエラー数系列を追加表示 | 中 |
| 5 | Demo App フロントエンド実装 | 中 |

### 3.5 懸念事項

- Must要件の未完了（OP-F-14, OP-F-15）は次スプリントで必ず対応
- 月額$1以下のコスト目標の検証が未実施
- 認証・認可の不在（デプロイ前に検討必要）

---

## 4. 受入判定

### プロダクトオーナー判定（鈴木）

| PBI ID | タイトル | SP | 判定 |
|--------|----------|---:|:----:|
| PBI-001 | Demo App インフラ基盤構築 | 5 | **受入** |
| PBI-002 | GET /posts | 3 | **受入** |
| PBI-003 | POST /posts | 3 | **受入** |
| PBI-004 | GET /posts/:id | 2 | **受入** |
| PBI-005 | DELETE /posts/:id | 2 | **受入** |
| PBI-006 | Lambda構造化ログ共通モジュール | 3 | **受入** |
| PBI-010 | OPインフラ基盤構築 | 5 | **受入** |
| PBI-011 | CloudWatchメトリクス取得API | 8 | **受入** |
| PBI-012 | CloudWatchログ取得API | 5 | **受入** |
| PBI-014 | Overview画面 | 5 | **受入** |
| PBI-016 | Endpoints画面 | 5 | **受入** |

**差戻: 0件**

**顧客条件:** 次スプリントで OP-F-14, OP-F-15, Logs画面（OP-S-04）の Must 要件を完成させること

---

## 5. プロダクトバックログの調整

### ステータス変更

- PBI-001〜006, PBI-010〜012, PBI-014, PBI-016: **Done**
- PBI-013（時間範囲セレクタ）: PBI-014実装時に完成 → **Done**

### 優先度変更

| PBI ID | 変更前 | 変更後 | 理由 |
|--------|--------|--------|------|
| PBI-017 | High | **Critical** | 顧客Must要件（OP-F-14） |
| PBI-018 | High | **Critical** | 顧客Must要件（OP-F-15） |
| PBI-020 | High | **Critical** | Logs画面の基本機能として必須 |

### 次スプリント優先 PBI

1. PBI-017: Endpoint Detail - エラー推移グラフ（5SP, Critical）
2. PBI-018: Endpoint Detail - ステータスコード内訳（5SP, Critical）
3. PBI-019: Logs画面 - ログ一覧（5SP, Critical）
4. PBI-020: Logs画面 - フィルタ機能（3SP, Critical）

---

## 6. 総括

Sprint 001 は計画 46SP に対して 46SP 完了（消化率 100%）。スプリントゴールを達成し、システム全体の開発基盤が確立されました。顧客からは条件付き受入を受け、次スプリントで Must 要件の残りを完成させることが求められています。
