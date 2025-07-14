import random

def generate_random_number():
    return random.randint(1, 100)

player1_number = generate_random_number()
player2_number = int(input("1~100 사이의 숫자를 입력해줘! : "))

count = 1
while True:
    if player1_number != player2_number:
        if player1_number < player2_number:
            print("너가 입력한 숫자보다 작아!")
            player2_number = int(input("다시 입력해줘! : "))
            count += 1
        else:
            print("너가 입력한 숫자보다 커!")
            player2_number = int(input("다시 입력해줘! : "))
            count += 1
    else:
        print("컴퓨터가 준 숫자는 ",player1_number, "이고",count,"번만에 맞췄어")
        break