# API 抓取寫入 SQL Server 主程式
import requests
import pyodbc
import math
from urllib.parse import urlencode

# --- 安全 float 轉換 ---
def safe_float(value, precision=None):
    try:
        f = float(value)
        if math.isnan(f) or not (-1e308 < f < 1e308):
            return 0.0
        return round(f, precision) if precision is not None else f
    except (ValueError, TypeError):
        return 0.0

# --- 清理欄位 ---
def clean_value(value, data_type, max_length=None, precision=None):
    if value in [None, "NaN", "nan", "", "null", "None_nan", "None_None", float('nan')]:
        return '' if data_type == 'str' else 0 if data_type == 'int' else 0.0
    try:
        if data_type in ['float', 'decimal']:
            return safe_float(value, precision)
        elif data_type == 'int':
            return int(value) if str(value).isdigit() else 0
        elif data_type == 'str':
            value = str(value).strip()
            return value[:max_length] if max_length and len(value) > max_length else value
    except (ValueError, TypeError):
        return '' if data_type == 'str' else 0 if data_type == 'int' else 0.0

# --- 固定參數 ---
fixed_params = {
    "comp": "C0A2",
    "rank_by": "DPT",
    "ctno_period_min": "None",
    "ctno_period_max": "None"
}

# --- 多組查詢條件（可擴充） ---
params_list = [
    {"參數1": "參數2", "參數3": "參數4", "參數5": "參數6"},

    # 可再加更多組查詢參數
]

# --- API 抓資料 ---
def fetch_data(query_params):
    base_url = "https://aicustomerinsight.公司網域.com.tw/get_matrix_tag"
    full_params = {**fixed_params, **query_params}
    url = f"{base_url}?{urlencode(full_params)}"
    try:
        response = requests.get(url, timeout=900)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API 錯誤：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ API 連線失敗：{e}")
        return None

# --- 查 DL130NO ---
def get_dl130no(cursor, params):
    query = f"""
        SELECT xxxxxno FROM xxxxx
        WHERE dimension = '{params['dimension']}'
        AND time_begin = '{params['time_begin']}'
        AND time_end = '{params['time_end']}'
    """
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else 0

# --- 寫入 DL131 ---
def save_to_sql(data, dl130no):
    conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=xxx.xxx.xx.xx;DATABASE=dbname;UID=account;PWD=password'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        table_columns = [
            "columns1", "columns2",
  
        ]

        column_types = {
            col: "str" if col in ["columns1", "columns2"]
            else "decimal" for col in table_columns
        }

        query = f"""
        INSERT INTO xxxxx (xxxxx, {', '.join(table_columns)})
        VALUES (?, {', '.join(['?' for _ in table_columns])})
        """

        for idx, item in enumerate(data):
            if 'MARA' not in item:
                item['MARA'] = ''
            cleaned_values = [
                clean_value(item.get(col), column_types[col], precision=2)
                for col in table_columns
            ]
            try:
                cursor.execute(query, dl130no, *cleaned_values)
            except Exception as ex:
                print(f"❌ 寫入第 {idx+1} 筆失敗：{item}")
                print(f"錯誤訊息：{ex}")
                raise

        conn.commit()
        print(f"✅ 成功寫入 DL131，dl130no={dl130no}，共 {len(data)} 筆")
    finally:
        cursor.close()
        conn.close()

# --- 主流程 ---
def main():
    conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=xxx.xxx.xx.xx;DATABASE=dbname;UID=account;PWD=password'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    for params in params_list:
        print(f"🔍 查詢參數：{params}")
        dl130no = get_dl130no(cursor, params)
        if not dl130no:
            print("⚠️ 查無對應 dl130no，略過此組")
            continue

        data = fetch_data(params)
        if data:
            save_to_sql(data, dl130no)
        else:
            print("⚠️ API 無資料")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
