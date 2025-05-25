import os
import sys
import webbrowser
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path
from waitress import serve
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

def setup_database():
    """データベースの初期設定"""
    db_path = os.path.join('db', 'vital.sqlite3')
    os.makedirs('db', exist_ok=True)
    
    # データベースが存在しない場合は作成
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA synchronous=FULL')
        conn.close()
    else:
        # 既存のDBにWALモードを適用
        conn = sqlite3.connect(db_path)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA synchronous=FULL')
        conn.close()

def setup_backup_dirs():
    """バックアップディレクトリの作成"""
    backup_dirs = ['backup/daily', 'backup/weekly', 'archive']
    for dir_path in backup_dirs:
        os.makedirs(dir_path, exist_ok=True)

def main():
    # アプリケーションのルートディレクトリを設定
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(app_dir)
    
    # データベースとバックアップの設定
    setup_database()
    setup_backup_dirs()
    
    # 環境変数の設定
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tempmon.settings_prod')
    
    # 開発サーバーを起動
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        execute_from_command_line(sys.argv)
    else:
        # 本番用サーバー（Waitress）を起動
        application = get_wsgi_application()
        # ブラウザを自動的に開く
        webbrowser.open('http://127.0.0.1:8000')
        # サーバーを起動
        serve(application, host='127.0.0.1', port=8000)

if __name__ == '__main__':
    main() 