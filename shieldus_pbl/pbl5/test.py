from dotenv import load_dotenv
import os

# 명시적으로 상위 폴더의 .env 경로 지정
load_dotenv(dotenv_path='c:/skshieldus26th/.env')

print("ID:", os.getenv("SECRET_ID"))
print("PASS:", os.getenv("SECRET_PASS"))
    