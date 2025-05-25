# 体温管理システム インストール手順

## 必要条件
- Windows 10/11
- Python 3.8以上
- pip（Pythonパッケージマネージャー）

## インストール手順

1. Pythonのインストール
   - [Python公式サイト](https://www.python.org/downloads/)からPython 3.8以上をダウンロード
   - インストール時に「Add Python to PATH」にチェックを入れる

2. プロジェクトのセットアップ
   - プロジェクトフォルダを任意の場所にコピー
   - コマンドプロンプトを管理者として実行
   - プロジェクトフォルダに移動
   ```
   cd プロジェクトフォルダのパス
   ```

3. 仮想環境の作成と有効化
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

4. 必要なパッケージのインストール
   ```
   pip install -r requirements.txt
   ```

5. データベースの初期化
   ```
   python manage.py migrate
   ```

6. テストデータの作成（オプション）
   ```
   python create_test_data.py
   ```

7. Windowsアプリケーションのビルド
   ```
   pyinstaller build_app.spec
   ```
   - ビルドが完了すると、`dist`フォルダに実行可能ファイルが作成されます
   - `dist/体温管理システム.exe`をダブルクリックして起動できます

## 注意事項
- 本番環境での使用時は、適切なセキュリティ設定を行ってください
- データベースのバックアップを定期的に取得することをお勧めします
- エラーが発生した場合は、以下を確認してください：
  - Pythonのバージョン
  - 必要なパッケージが正しくインストールされているか
  - データベースの接続設定

## トラブルシューティング
1. パッケージのインストールでエラーが発生する場合
   ```
   pip install --upgrade pip
   ```
   を実行してから再度インストールを試してください

2. データベースのエラーが発生する場合
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   を実行してください

3. アプリケーションが起動しない場合
   - アンチウィルスソフトの設定を確認
   - 管理者権限で実行を試す
   - 別のポートを指定して起動する場合は、`run_app.py`を編集 