wallet = []
bill = []

xxb, yyb = input("지폐 가로, 세로 길이 순서대로 입력: ").split(",")
bill = [int(xxb), int(yyb)]

xxw, yyw = input("지갑 가로, 세로 길이 순서대로 입력: ").split(",")
wallet = [int(xxw), int(yyw)]


answer = 0

def flip():
    """지폐 가로 세로 반 접는 함수"""
    garo = bill[0] / 2
    sero = bill[1] / 2
    bill[0] = garo
    bill[1] = sero
    global answer
    print("지폐를 반으로 접습니다.")
    answer += 1
    return bill[0], answer



while True:
    if bill[0] <= wallet[0] and bill[1] <= wallet[1]:
        print("지폐를 지갑에 넣을 수 있습니다.")
        break
    else:
        flip()

print("지폐를 지갑에 넣기 위해 반으로 접은 횟수:", answer)

