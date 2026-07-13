import sys
print("start...")

while True:
    print("Menu Start ")
    cmd = input("input cmd: ")
    print(f"입력한 정보는 {cmd}")
    if(cmd == "q"):
        print("bye")
        sys.exit()


print("end...")