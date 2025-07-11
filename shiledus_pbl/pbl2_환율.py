import requests

# App ID (당신이 발급받은 것)
app_id = "a26586dbc1bb426087dbce7532590730"

# 예: USD 기준 환율 데이터 요청
url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
print("환율 목록")
for currency, rate in data["rates"].items():
        print(f"{currency}: {rate}")
data = input("변환할 통화, 목표 통화, 금액을 입력하세요 (예: USD,KRW,100): ")
from_currency, to_currency, amount = data.strip().split(',')

# 금액을 숫자로 변환
amount = float(amount)

# 출력 확인
print(f"변환할 통화: {from_currency}")
print(f"목표 통화: {to_currency}")
print(f"금액: {amount}")
