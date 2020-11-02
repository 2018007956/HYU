# 파일 이름 변경 코드
# 구현했지만, 얼굴인식 과제에서 전혀 쓸 필요 없었다
import re
import sys
from os import rename, listdir
import os

path = ('C:\\Users\\LG\\Desktop\\faces')
files = listdir('C:\\Users\\LG\\Desktop\\faces')

count=0
pren=''
for name in files:
    # 파이썬 실행파일명은 변경하지 않음
    if sys.argv[0].split('\\')[-1]==name:
        continue
    num = re.findall('\d+',name)
    numb = ''.join(num) # 리스트를 str로 변환

    n = name
    n = n.replace(numb,'').replace('.jpg','')
    # 다른 사람일때만 count+1
    if pren != n:
        count += 1
    if numb>str(0): # 빈리스트 제외 (실행파일)
        new_name=str(count)+'_'+numb[-3:]+'.jpg'
        rename(os.path.join(path,name),os.path.join(path,new_name))
    pren = n


''' 파일 이름 :
1_001
2_001
3_001 3_002 3_003
4_001
5_001 5_002
6_001

'''
