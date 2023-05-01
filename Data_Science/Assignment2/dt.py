import sys
import math
import numpy as np
import pandas as pd

training_file = sys.argv[1]
test_file = sys.argv[2]
output_file = sys.argv[3]

# Read Input Files
data = pd.read_csv(training_file, sep='\t', header = 0)
features = data.columns[:-1]
target = data.columns[-1]

Minimum_Gain = len(data) * 0.00007
print('Minimum Gain:',Minimum_Gain)

# Information Gain
def Info(data): 
    m, p = np.unique(data, return_counts = True)
    Entropy = sum([-(p[i]/sum(p))*math.log2(p[i]/sum(p)) for i in range(len(m))])
    return Entropy

# Gain Ratio: normalization to information gain
def GainRatio(data, split_attr):
    total_entropy = Info(data[target])

    # vals: values, D: counts for each values
    vals,D = np.unique(data[split_attr], return_counts=True)
    weighted_entropy = sum([(D[i]/sum(D))*
                            Info(data.where(data[split_attr]==vals[i]).dropna()[target]) for i in range(len(vals))])
    
    SplitInfo = sum([-(D[i]/sum(D))*math.log2(D[i]/sum(D)) for i in range(len(vals))])
    Gain = total_entropy - weighted_entropy

    GainRatio = Gain / SplitInfo 
    return GainRatio


def build_tree(data, features, parent_label):
    # 1. target label이 1개 일 경우
    if len(np.unique(data[target]))==1: 
        return np.unique(data[target])[0] 
    # 2. Empty features
    elif len(features)==0:
        return parent_label
    # Build Tree
    else:
        parent_label = np.unique(data[target])[np.argmax(np.unique(data[target], return_counts=True)[1])]
        
        # Calculate Gain Ratio and Find max value feature to split data
        cal_GainRatio = [GainRatio(data, feature) for feature in features]
        best_feature = features[np.argmax(cal_GainRatio)]

        dt = {best_feature:{}}   
        features = [x for x in features if x!=best_feature]

        # Pre-Pruning by Setting Minimum gain: length of data x 0.0001
        # If it doesn't exceed the minimum gain, it no longer splits and currently has the most label returns 
        if cal_GainRatio[np.argmax(cal_GainRatio)] < Minimum_Gain:
            return parent_label
        
        else:
            for i in np.unique(data[best_feature]):
                divided_data = data.where(data[best_feature]==i).dropna()

                child_tree = build_tree(divided_data, features, parent_label)
                dt[best_feature][i] = child_tree
        
        return dt

def get_label_average(feature, input, feature_order):
    # 들어온 feature 전까지의 피쳐들(트리를 따라 split된 순서대로)의 값을 input과 같은 값들만 남김
    # parent tree 부분을 input 값으로 고정 (다른 값들 모두 drop)
    global data 
    
    df = pd.DataFrame(data)
    idx = feature_order.index(feature)

    for i in feature_order[:idx]:
        df = df.where(df[i] == input[i]).dropna()

    # Majority voting
    get_label = df.groupby(df.columns[-1]).size().sort_values(ascending=False).index[0]

    return get_label


def classifier(dt, input, split_feature_order): # input: one element to be classified
    if type(dt) is not dict: # If there is only one label because of pre-pruning
        return dt

    feature = list(dt.keys())[0] # root feature
    subtree_dict = list(dt.values())[0] 
    input_value = subtree_dict.get(input.get(feature))
    
    split_feature_order.append(feature)

    if input_value == None:
        return get_label_average(feature, input, split_feature_order)
    
    if type(input_value) is not dict:
        return input_value 
    
    return classifier(input_value, input, split_feature_order)


##### Main #####
tree = build_tree(data, features, '')

# load test data
test_data = pd.read_csv(test_file, sep='\t', header=0)

# Write txtfile
with open(output_file, 'w') as f:
    for feature in features:
        f.write(f'{feature}\t')
    f.write(f'{target}\n')

    for idx, row in test_data.iterrows():
        label = classifier(tree, row, split_feature_order=[]) 
        for value in row.values:
            f.write(f'{value}\t')
        f.write(f'{label}\n')