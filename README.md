# Enterprise Data Tools

本專案收錄企業內部資料處理與自動化任務的 Python 工具腳本，包括：

- SQL Server ➜ MySQL 的大批量資料遷移與備份工具
- API 抓取並寫入 SQL Server 的自動化腳本
- 資料備份與壓縮流程（使用 WinRAR）

---

## 📁 專案結構總覽

| 資料夾         | 說明                                           |
|----------------|------------------------------------------------|
| `/migration`   | SQL Server ➜ MySQL 資料遷移工具與備份腳本            |
| `/fetch_api`   | 批次查詢 API 並自動寫入 SQL Server 的腳本         |

---

## 📦 技術使用

- Python（pandas, requests, sqlalchemy, pyodbc）
- SQL Server / MySQL 資料庫
- WinRAR（自動壓縮備份）

---

## 📂 如何使用

1. 請先根據 `.env.example` 設定環境變數
2. 進入各資料夾執行對應的腳本
3. 詳情請參閱各資料夾內的 `README.md`

---

## 🙋‍♂️ 作者

Po Cheng Shih（施柏丞）｜後端開發 & 資料流程設計