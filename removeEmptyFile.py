import os

path = "D:\\CCCCcomputer\\2020_2\\컴퓨터보안\\과제\\assignment#2\\opcode\\1\\"
files = os.listdir(path)

for file in files:
    if os.stat(path+file).st_size == 0: # 빈 파일이면 삭제
        print(file)
        os.remove(path+file)
