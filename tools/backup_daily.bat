@echo off
setlocal

:: バックアップキーの設定（実際の運用時は変更してください）
set KEY=your_backup_key_here

:: 日付を取得
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set DATE=%%c%%a%%b
)

:: バックアップディレクトリの作成
if not exist "backup\daily" mkdir "backup\daily"

:: SQLiteデータベースのダンプと圧縮
sqlite3 "db\vital.sqlite3" .dump | 7za a -si "backup\daily\daily_%DATE%.7z" -p%KEY%

:: 古いバックアップの削除（14日以上前のファイル）
forfiles /P "backup\daily" /M *.7z /D -14 /C "cmd /c del @path"

echo 日次バックアップが完了しました。 