# Purple Archive APIサーバクライアント

<https://github.com/tsubasa283paris/purple-archive-server> のAPIを呼び出す、またはデータベースを操作するためのPythonプログラムツール。  
プロジェクト概要は <https://github.com/tsubasa283paris/purple-archive> を参照。

## 環境構築

動作確認済み環境はWSL2。

1. 実行に必要なPIPパッケージをインストールする。  
   ```bash
   pip install -r requirements.txt
   ```

1. データベースの認証情報を適宜 `db.json` に入力する。

1. ユーザ情報を適宜 `login.json` に入力する。

## 実行

各Pythonプログラムの `-h` コマンドライン引数で確認されたし。
