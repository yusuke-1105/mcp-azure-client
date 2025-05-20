# Azure MCP クライアント

Azureと連携するために特化したModel Context Protocol（MCP）クライアントです。本アプリケーションでは、対話型コマンドラインインターフェイスを通じてAzure MCPサーバー上のツールを一覧表示し、実行できます。

## 機能

- MCPプロトコルを使用してAzure MCPサーバーに接続
- 利用可能なツールの一覧表示と詳細情報（説明、パラメーター）の取得
- 対話形式でツールを実行し、必要なパラメーターを入力
- Dockerコンテナーとしてパッケージ化し、環境依存なく実行可能

## 要件

- Python 3.12以上
- 必要なPythonパッケージ:
  - `mcp`: Model Context Protocolライブラリ
  - `uv`: 依存管理ライブラリ
- Docker（コンテナー実行用）
- Node.js & npm（Azure MCPサーバー接続時に必要）

## 使い方

### Docker Compose（推奨）

1. プロジェクトルートでコンテナーを起動します。

   ```bash
   docker compose up -d
   ```

2. 初回起動時のみ、コンテナー内でAzure CLIにログインします。

   ```bash
   docker compose exec mcp-client az login
   ```

3. コンテナー内でクライアントを起動し、ログを確認します。

   ```bash
   docker compose exec mcp-client python3 mcp-client.py
   ```

4. サービスを停止するには、`Ctrl+C`を押したあと、次のコマンドを実行します。

   ```bash
   docker compose down
   ```

### ローカルインストール

1. 依存パッケージをインストールします。

   ```bash
   pip install -r requirements.txt
   ```

2. Node.jsとnpmがインストールされていることを確認してください。

3. クライアントを実行します。

   ```bash
   python mcp-client.py
   ```

## 動作原理

1. `npx`を使用して`@azure/mcp`パッケージを起動し、Azure MCPサーバーに接続します。
2. 接続後、以下の操作が可能です。
   - ツール一覧の表示（オプション1）
   - 指定番号のツール実行（オプション2）
   - アプリケーション終了（オプション3）
3. ツール呼び出し時に、必要なパラメーターを順に入力します。

## コード概要

- `MCPClient`クラス: サーバー接続と通信処理を実装
- `list_and_call_tools`関数: 対話型インターフェイスを制御
- 各種ヘルパー関数: ツール定義の展開と表示
- `main`関数: 実行フローを管理

## プロジェクト構成

```plaintext
.
├── Dockerfile            # コンテナー定義
├── docker-compose.yml    # Docker Compose設定
├── mcp-client.py         # メインアプリケーション
└── requirements.txt      # Python依存パッケージ一覧
```