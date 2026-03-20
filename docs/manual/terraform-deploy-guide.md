# Terraform インフラ構築手順書

本手順書は、`aws-observability-dashboard/infra` 配下の Terraform コードを使用して AWS 上にインフラを構築するための手順を説明します。

---

## 前提条件

| 項目 | 要件 |
|---|---|
| OS | Linux (Ubuntu/WSL2) |
| AWS CLI | v2 以上がインストール済みであること |
| AWS アカウント | 有効な AWS アカウントおよび管理者権限を保有していること |
| Terraform CLI | 本手順でインストールする |

---

## 手順 1: Terraform CLI のインストール

HashiCorp 公式の APT リポジトリから Terraform をインストールします。

### 1-1. 必要パッケージのインストール

- **目的**: HashiCorp リポジトリの GPG 署名検証や APT ソース管理に必要なツールを導入する。
- **実行結果**: `gnupg`（GPG 鍵の管理ツール）と `software-properties-common`（APT リポジトリ管理ツール）がシステムにインストールされる。

```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
```

### 1-2. HashiCorp GPG キーの追加

- **目的**: HashiCorp が配布するパッケージの正当性を検証するための公開鍵をシステムに登録する。
- **実行結果**: `/usr/share/keyrings/hashicorp-archive-keyring.gpg` に HashiCorp の GPG 公開鍵が保存され、以降のパッケージダウンロード時に改ざん検知が可能になる。

```bash
wget -O- https://apt.releases.hashicorp.com/gpg | \
  gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
```

### 1-3. HashiCorp リポジトリの登録

- **目的**: `apt-get install` で Terraform をインストールできるように、HashiCorp の APT リポジトリをパッケージソースに追加する。
- **実行結果**: `/etc/apt/sources.list.d/hashicorp.list` が作成され、APT が HashiCorp のリポジトリからパッケージを検索・取得できるようになる。

```bash
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
  https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list
```

### 1-4. Terraform のインストール

- **目的**: Terraform CLI 本体をインストールする。
- **実行結果**: `terraform` コマンドがシステムに追加され、ターミナルから実行可能になる。

```bash
sudo apt-get update && sudo apt-get install -y terraform
```

### 1-5. インストール確認

- **目的**: Terraform が正しくインストールされ、コマンドとして実行できることを確認する。
- **実行結果**: `Terraform vX.X.X` のようにバージョン番号が表示されればインストール成功。表示されない場合はインストール手順を見直す。

```bash
terraform --version
```

---

## 手順 2: AWS 認証の設定

Terraform が AWS リソースを操作するために、AWS 認証情報を設定します。

> **セキュリティに関する注意**: AWS はルートユーザーのアクセスキー作成や長期的な IAM ユーザーキーの使用を非推奨としています。可能な限り方法 A（IAM Identity Center）を使用してください。

### 方法 A: IAM Identity Center (SSO) を使用する（推奨）

AWS IAM Identity Center は一時的なセキュリティ認証情報を自動発行するため、長期的なアクセスキーが不要です。

#### A-1. AWS コンソールで IAM Identity Center を有効化する

1. AWS マネジメントコンソールにログインし、**IAM Identity Center** を開く
2. **「有効にする」** をクリックする
3. インスタンスタイプの選択画面が表示された場合は **「AWS Organizations で IAM Identity Center を有効にする」**（組織インスタンス）を選択する
   - AWS CLI / Terraform での一時認証情報取得には組織インスタンスが必要です
   - IAM Identity Center・AWS Organizations ともに追加料金はかかりません
4. **「ユーザー」** → **「ユーザーを追加」** から作業用ユーザーを作成する
   - メールアドレスの入力が必須。招待メールが届くので実在するアドレスを使用すること
5. **「許可セット」** → **「許可セットを作成」** で `AdministratorAccess` の許可セットを作成する
   - 本番環境では最小権限の許可セットを使用すること
6. **「AWSアカウント」** から対象アカウントを選択し、作成したユーザーと許可セットを割り当てる
7. IAM Identity Center の**ダッシュボード（トップ画面）** に表示されている **「アクセスポータルの URL」** を控えておく

#### A-2. ローカル CLI に SSO プロファイルを設定する

```bash
aws configure sso
```

以下の項目を入力します:

| 項目 | 入力値 |
|---|---|
| SSO session name | admin-access-sso |
| SSO start URL | https://d-9567ae5634.awsapps.com/start |
| SSO region | `ap-northeast-1` |
| SSO registration scopes | `sso:account:access`（デフォルトのままEnter） |

ブラウザが自動的に開くので、AWS コンソールで認可を承認します。その後 CLI に戻り、以下を入力します:

| 項目 | 入力値 |
|---|---|
| CLI default client Region | `ap-northeast-1` |
| CLI default output format | `json` |
| CLI profile name | 任意のプロファイル名（例: `dev`） |

#### A-3. SSO ログインを実行する

```bash
aws sso login --profile dev
```

ブラウザが開き、承認が完了すると一時的な認証情報が自動発行されます。

#### A-4. プロファイルを指定して Terraform を実行する

```bash
export AWS_PROFILE=dev
terraform plan
```

またはコマンドごとに指定する場合:

```bash
AWS_PROFILE=dev terraform plan
```

> **補足**: 一時認証情報の有効期限が切れた場合は `aws sso login --profile dev` を再実行してください。

---

### 認証確認

以下のコマンドで認証が正しく設定されているか確認します。

```bash
aws sts get-caller-identity
```

アカウント情報（Account、Arn、UserId）が表示されれば認証成功です。

---

## 手順 3: Terraform 初期化

Terraform の作業ディレクトリに移動し、初期化を実行します。

```bash
cd aws-observability-dashboard/infra
terraform init
```

このコマンドにより以下が実行されます:

- AWS プロバイダー (`hashicorp/aws ~> 5.0`) のダウンロード
- バックエンドの初期化
- プラグインのインストール

「Terraform has been successfully initialized!」と表示されれば完了です。

---

## 手順 4: 構成の検証（ドライラン）

実際にリソースを作成せずに、Terraform コードの妥当性を検証します。

### 4-1. 構文チェック

```bash
terraform validate
```

構文エラーがないことを確認します。

### 4-2. 実行計画の確認

```bash
terraform plan
```

このコマンドで、作成・変更・削除されるリソースの一覧が表示されます。

本プロジェクトでは以下のリソースが作成されます:

| リソース種別 | 内容 |
|---|---|
| DynamoDB テーブル | `posts`（Demo App 用） |
| Lambda 関数（Demo App） | `get_posts`, `get_post`, `delete_post`, `create_post` |
| Lambda 関数（OP） | `get_logs`, `get_metrics` |
| API Gateway（Demo App） | Demo App 用 REST API |
| API Gateway（OP） | Observability Platform 用 REST API |
| IAM ロール・ポリシー | Lambda 実行用ロール（Demo App 用、OP 用） |

---

## 手順 5: デプロイの実行

検証結果に問題がなければ、実際に AWS 上にリソースを作成します。

```bash
terraform apply
```

実行計画が表示された後、確認プロンプトが表示されます。

```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value:
```

`yes` と入力して確定します。

---

## 手順 6: デプロイ後の確認

デプロイ完了後、作成されたリソースの情報を確認します。

```bash
terraform output
```

以下の情報が出力されます:

- DynamoDB テーブル名・ARN
- API Gateway ID・実行 ARN
- IAM ロール ARN・ロール名

---

## リソースの削除

作成したリソースが不要になった場合、以下のコマンドで全リソースを削除できます。

```bash
terraform destroy
```

確認プロンプトで `yes` と入力すると、Terraform で管理しているすべてのリソースが削除されます。

---

## 注意事項

- **コスト**: Lambda・DynamoDB・API Gateway はいずれも AWS 無料利用枠がありますが、利用状況によっては課金される可能性があります。デプロイ前に [AWS 料金計算ツール](https://calculator.aws/) で確認してください。
- **State ファイル**: 現在の構成では `terraform.tfstate` がローカルに保存されます。チーム開発の場合は S3 バックエンドの設定を検討してください。
- **シークレット管理**: アクセスキーをリポジトリにコミットしないでください。`.gitignore` に認証情報ファイルが含まれていることを確認してください。
- **リージョン**: デフォルトのリージョンは `ap-northeast-1`（東京）です。変更する場合は `terraform.tfvars` ファイルで `aws_region` を指定してください。
