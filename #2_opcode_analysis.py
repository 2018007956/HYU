import glob
import numpy as np
import pandas as pd
from math import log
from scipy import spatial
import math

path = "D:\\CCCCcomputer\\2020_2\\컴퓨터보안\\과제\\assignment#2\\opcode\\test3\\*.txt"
files = glob.glob(path)

corpus =[]
# 파일을 통째로 str로 저장
for file in files:
    with open(file,"r") as f:
        doc = []
        for word in f:
            doc.append(word.rstrip('\n'))
        corpus.append(' '.join(doc))

vocab = list(set(w for x in corpus for w in x.split()))
vocab.sort()

N = len(corpus) # 총 문서의 수

def tf(t, d):
    return math.log(d.count(t)+1)

def idf(t):
    df = 0
    for doc in corpus:
        df += t in doc
    return log(N/(df + 1))

def tfidf(t, d):
    return tf(t,d)* idf(t)


result = []
for i in range(N):
    result.append([])
    d = corpus[i]
    for j in range(len(vocab)):
        t = vocab[j]

        result[-1].append(tfidf(t,d))

result = np.array(result)
tfidf_ = pd.DataFrame(result, columns = vocab)
# print(tfidf_)


analysis=[]
malware = [0, 2.56591, 0.155082, 0.126886, 0.39755]
for n in range(len(corpus)):
    opcode_list = np.split(result[n],len(result[n]))

    re_opcode_list =[]
    need_only = ['bsr', 'and', 'clc', 'aad', 'call']
    for opcode in need_only:
        if opcode in vocab:
            idx = vocab.index(opcode)
            re_opcode_list.append(float(opcode_list[idx]))
        else:
            re_opcode_list.append(0)

    # cosine similarity
    cosine_sim = 1 - spatial.distance.cosine(re_opcode_list, malware)

    analysis.append(cosine_sim)

# 정확도 분석
notmal = 0
malware = 0
for i in range(len(analysis)):
    if analysis[i] > 0:
        malware += 1
    else:
        notmal += 1

print('정상파일 개수:',notmal)
print('악성파일 개수:',malware)