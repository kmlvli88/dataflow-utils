# SQL Server ➜ MySQL 資料遷移與備份工具

本工具可將 SQL Server 中的大量資料表分批遷移至 MySQL，同時支援 MySQL 資料庫備份與壓縮。

---

## 功能說明

- 從 SQL Server 資料庫抓取資料（支援主鍵排序與分批）
- 自動型別對應（整數、浮點、字串）
- 寫入 MySQL（使用 SQLAlchemy）
- 使用 `mysqldump` 匯出 .sql 檔
- 自動壓縮成 `.rar` 備份（透過 WinRAR）

---

## 使用方式

### 1. 設定資料庫連線資訊（可改用 .env）
你可以在腳本中自行填入帳號，或使用 `.env` 檔（建議搭配 dotenv 套件）

### 2. 執行主程式

```bash
python sqlserver_to_mysql_migration.py
