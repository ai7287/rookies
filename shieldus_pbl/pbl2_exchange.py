import requests

# App ID
app_id = "a26586dbc1bb426087dbce7532590730"

url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"

response = requests.get(url)

if response.status_code != 200:
    print("환율 데이터를 가져오는 데 실패했습니다.")
    exit()

data = response.json()
rates = data["rates"]

# 주요 통화 10개국
main_currencies = ['USD', 'KRW', 'EUR', 'JPY', 'CNY', 'GBP', 'AUD', 'CAD', 'CHF', 'HKD']

# 환율 출력
print("\n[주요 통화 환율 (기준: USD)]")
for currency in main_currencies:
    if currency in rates:
        print(f"{currency}: {rates[currency]:,.2f}")

# 사용자 입력 받기
while True:
    user_input = input("\n변환할 통화, 목표 통화, 금액을 입력하세요 (예: USD,KRW,100) 또는 q 입력 시 종료: ")
    
    if user_input.lower() == 'q':
        print("환율 계산기를 종료합니다.")
        break

    try:
        from_currency, to_currency, amount = user_input.strip().split(',')
        amount = float(amount)

        # 환율 계산
        usd_amount = amount / rates[from_currency] if from_currency != "USD" else amount
        converted_amount = usd_amount * rates[to_currency]

        # 결과 출력
        print(f"\n[결과]")
        print(f"{amount:,.2f} {from_currency} → {converted_amount:,.2f} {to_currency}")
    except ValueError:
        print("입력 형식이 잘못되었습니다. 예: USD,KRW,100")