# API 抓取與寫入 SQL Server 工具

此目錄為根據固定參數批次查詢 API，並自動寫入 SQL Server 指定資料表（DL121）。

## 功能：
- 呼叫 API (多組條件參數)
- 對應資料表 DL120 查詢主鍵
- 寫入 DL121（處理欄位與格式清洗）

執行：
```bash
python fetch_api_to_sql.py
```
