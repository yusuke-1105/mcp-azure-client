# MCP Azure クライアント

PythonベースのModel Context Protocol (MCP) クライアントで、Azure AIサービスと連携するために設計されています。このアプリケーションは、Azure MCPサーバーへ接続し、利用可能なツールを対話型コマンドラインインターフェイスから呼び出す便利な方法を提供します。

## 特徴

- MCPプロトコルを使ってAzure MCPサーバーに接続
- 利用可能なツールの一覧表示（説明・必要パラメーター付き）
- パラメーター入力によるツールの対話的実行
- Dockerによる一貫した環境でのデプロイ

## 必要要件

- Python 3.12以上
- 必要なPythonパッケージ：
  - `mcp`: Model Context Protocolライブラリ
  - `uv`: 依存関係管理
- Docker（コンテナー実行用）
- Node.js & npm（Azure MCPサーバー接続用）

## 使い方

### Docker Compose（推奨）

本アプリケーションはコンテナー化されており、Docker Composeを使うことで依存関係や環境構築を自動で管理できます。

1. プロジェクトディレクトリでサービスを起動：

   ```bash
   docker compose up -d
   ```

2. これでコンテナーのビルド・アプリケーションの起動・ログの表示が行われます。

   ```bash
   docker compose exec mcp-client python3 mcp-client.py
   ```

3. アプリケーションが起動すると、自動的にAzure MCPサーバーへ接続し、クライアントインターフェイスが表示されます。

4. サービスを停止するには、`Ctrl+C`を押した後、以下を実行：

   ```bash
   docker compose down
   ```

### ローカルインストール

ローカルで実行したい場合：

1. 依存関係をインストール：

   ```bash
   pip install -r requirements.txt
   ```

2. システムにnpmがインストールされていることを確認

3. クライアントを実行：

   ```bash
   python mcp-client.py
   ```

## 動作概要

1. アプリケーションはnpxで`@azure/mcp`パッケージを実行し、Azure MCPサーバーへ接続します
2. 接続後、以下が可能です：
   - 利用可能なツールの一覧表示（1番）
   - ツール番号指定での実行（2番）
   - アプリケーション終了（3番）
3. ツール実行時は、必要・任意パラメーターの入力を求められます

## コード概要

`mcp-client.py`ファイルには以下が含まれます：

- `MCPClient`クラス：サーバー接続ロジック
- `list_and_call_tools`関数：対話型CLIインターフェイス管理
- ツール定義の展開・表示用ヘルパー関数
- アプリケーション全体の流れを制御するメイン関数

## プロジェクト構成

```plaintext
.
├── Dockerfile            # コンテナー定義
├── docker-compose.yml    # Docker Compose設定
├── mcp-client.py         # メインアプリケーションコード
└── requirements.txt      # Python依存パッケージ
```
