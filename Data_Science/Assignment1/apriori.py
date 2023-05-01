import sys
import numpy as np
import itertools 

SUPmin = float(sys.argv[1])
input_file = sys.argv[2]
output_file = sys.argv[3]

# Read Input Files
items = []
with open(input_file, mode='r') as f:
    for transaction in f:
        items.append(transaction.strip().split('\t'))
num_of_transaction = len(items)

# Check if all elements in transaction
def check_in_trans(chk, trans):
    cnt = 0
    for ele in chk:
        if ele in trans:
            cnt += 1
    return cnt==len(chk)

# Calculate candidates support probability
# Two input type 1)'1': string, 2) ('1','2',): tuple
def count_candidates(Candidate):
    for trans in items:
        for i in Candidate:
            if type(i) is np.str_: # element is one string
                if i in trans:
                    Candidate[i]+=1
            elif check_in_trans(i, trans): # i is tuple (more than two)
                Candidate[i]+=1
    Candidate = {k:(v/num_of_transaction)*100 for k,v in Candidate.items()}
    return Candidate

# Find association rules and calculate confidence
def cal_associative_item_set(List):
    with open(output_file, mode='a') as f:
        for k,support in List.items():
            # if len(k)>=2: #-> k=2부터 이 함수 호출하기 때문에 all satisfy    
            for n in range(1,len(k)):
                for item_set in list(itertools.combinations(k,n)):
                    associative_item_set = list(set(k)-set(item_set))
                    union = list(item_set) + associative_item_set
                    print(f'{{{str(list(map(int,item_set)))[1:-1]}}}\t{{{str(list(map(int,associative_item_set)))[1:-1]}}}',end='\t', file=f)

                    item_set = {tuple(item_set):0} #생성할때 여러 원소를 튜플 하나에 넣어야함
                    associative_item_set = {tuple(associative_item_set):0}
                    item_set = count_candidates(item_set)
                    b = item_set[next(iter(item_set))]
                    
                    union = {tuple(union):0}
                    union = count_candidates(union)
                    a = union[next(iter(union))]
                    
                    confidence = (a/b)*100
                    print(f'{support:.2f}\t{confidence:.2f}', file=f)  


# Scan DB once to get frequent 1-itemset
Candidate = {x:0 for x in np.unique(np.array(list(itertools.chain(*items))))}
Candidate = count_candidates(Candidate)
List = {key:value for key,value in Candidate.items() if value>=SUPmin}

k=2
infrequent_set = {}
while True:
    # Generate candidate itemsets of length k from frequent itemsets of length (k-1)
    single_items = np.unique(np.array(list(List.keys())))
    Candidate = {x:0 for x in list(itertools.combinations(single_items, k))}
    
    # Terminate when no candidate set can be generated
    if not Candidate: 
        break 
    # Pruning 1st) Before candidate generation: rm if include infrequent itemset
    if infrequent_set: # 3rd scan 부터
        Candidate = {k:v for k,v in Candidate.items() if k not in infrequent_set}
    
    Candidate = count_candidates(Candidate)
    # print('Candidate: ',Candidate)

    # Pruning 2nd) After candidate generation: rm if less than SUPmin
    List = {key:value for key,value in Candidate.items() if value>=SUPmin}  
    infrequent_set = dict(set(Candidate.items()) - set(List.items()))
    # print('List: ',List)

    # Terminate when no frequent set can be generated
    if not List: 
        break

    # Write output file
    cal_associative_item_set(List)

    k+=1