import sys
print("start ----")

input_data = "카드3"


##되도록 하단 if문 돌기 이전에 예외 처리후 종료
if(input_data != "카드1" and input_data != "카드2" and input_data != "카드3"):
    sys.exit()

if(input_data == "카드1"):
    print("카드1 업무 진행")
elif(input_data == "카드2"):
    print("카드2 업무 진행")
elif(input_data == "카드3"):
    print("카드3 업무 진행")

print("end ----")