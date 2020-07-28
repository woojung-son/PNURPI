#!/usr/bin/python3 
from hyperparams import *
from rawdata_preprocessing import read_RPI_pairSeq, read_NPInter_pairSeq
from copy import deepcopy
import numpy as np

isPrint = True

# Reduced Protein letters(7 letters)
def get_reduced_protein_letter_dict():
    rpdict = {}
    reduced_letters = [["A","G","V"],
                       ["I","L","F","P"],
                       ["Y","M","T","S"],
                       ["H","N","Q","W"],
                       ["R","K"],
                       ["D","E"],
                       ["C"]]
    changed_letter = ["A","B","C","D","E","F","G"]
    for class_idx, class_letters in enumerate(reduced_letters):
        for letter in class_letters:
            rpdict[letter] = changed_letter[class_idx]
                
    #rpdict = {"A" : ["A","G","V"], "B" : ["I","L","F","P"], ... }
    return rpdict

# Improved CTF 
class improvedCTF:
    def __init__(self, letters, length):
        self.letters = letters
        self.length = length
        self.dict = {}
        self.generate_feature_dict()
        
    def generate_feature_dict(self):
        def generate(cur_key, depth):
            if depth == self.length:
                return
            for k in self.letters:
                next_key = cur_key + k
                self.dict[next_key] = 0
                generate(next_key, depth+1)
                
        generate(cur_key="",depth=0)
        
        if isPrint:
            print("iterate letters : {}".format(self.letters))
            print("number of keys  : {}".format(len(self.dict.keys())))
        
    
    def get_feature_dict(self):
        for k in self.dict.keys():
            self.dict[k] = 0
            
        return deepcopy(self.dict)

    
# CTF feature processing
def preprocess_feature(x, y, npz_path): # /data/npz/RPI369.npz 파일을 생성하는 함수.
# read_RPI_pairSeq(size) 의 return값 X, Y가 각각 x, y
# X : 2차원 배열 [[protein value1, rna value1], [protein value2, rna value2], ... ]
# Y : 1차원 배열. label의 배열 [1, 1, 1, ... , 0, 0, 0]
    
    def min_max_norm(a):
        a_min = np.min(a)
        a_max = np.max(a)
        return (a - a_min)/(a_max - a_min)
    
    rpdict = get_reduced_protein_letter_dict()
    feature_x = []
    r_mer = 4
    r_CTF = improvedCTF(letters=["A","C","G","U"],length=r_mer)
    #r_feature_dict = r_CTF.get_feature_dict()
    
    p_mer = 3
    p_CTF = improvedCTF(letters=["A","B","C","D","E","F","G"],length=p_mer)
    #p_feature_dict = p_CTF.get_feature_dict()
    
    x_protein = []
    x_rna = []
        
    for idx, (pseq, rseq) in enumerate(x): # pseq : protein value / rseq : RNA value
        
        r_feature_dict = r_CTF.get_feature_dict()
        p_feature_dict = p_CTF.get_feature_dict()
        rpseq = []
        # 이 for loop 에서 rpdict의 규칙에 의해 각각의 알파벳을 reduced set으로 간소화시킨다 e.g. ["A","G","V"] -> "A"
        # 근데 X일 때는 그대로 저장함!!!
        for p in pseq: # MQKGNFRNQRKTVKCFNCGKEGHIAKNCRAPRKKGCWKCGKEGHQMKDCTERQANX 의 각 알파벳을 p로 받으면서 순회한다.
            if p=="X": # MQKGNFRNQRKTVKCFNCGKEGHIAKNCRAPRKKGCWKCGKEGHQMKDCTERQANX 에서 X가 포함되어 있으면 ~?
                rpseq.append(p)
            else:
                rpseq.append(rpdict[p])
                
        pseq = rpseq
        temp_pseq = ""
        for p in pseq:
            temp_pseq += p
        pseq = temp_pseq
        
        # 이 for loop 은 모든 값이 0으로 초기화된 p_feature_dict에서, 현재 protein의 패턴을 분석하면서 각 요소가 얼마나 나오는지 세는 것이다.
        for mer in range(1,p_mer+1):
            for i in range(0,len(pseq)-mer):
                pattern = pseq[i:i+mer]
                try:
                    p_feature_dict[pattern] += 1
                except:
                    continue
                #print(pattern)
        
        # 이 for-loop 도 마찬가지.
        for mer in range(1,r_mer+1):
            for i in range(0,len(rseq)-mer):
                pattern = rseq[i:i+mer]
                try:
                    r_feature_dict[pattern] += 1
                except:
                    continue
                #print(pattern)
        
        
        
        p_feature = np.array(list(p_feature_dict.values()))
        p_feature = min_max_norm(p_feature) #각각의 최소값을 0, 최대값을 1로 해서 그 사이값을 소수로 나타내는 것이다
        
        r_feature = np.array(list(r_feature_dict.values()))
        r_feature = min_max_norm(r_feature)
        
        
        x_protein.append(p_feature)
        x_rna.append(r_feature)
        
        if isPrint : 
            print("CTF preprocessing ({} / {})".format(idx+1, len(x)))
            #print(r_feature)
            
                
    
    x_protein = np.array(x_protein)
    x_rna = np.array(x_rna)
    y = np.array(y)
    np.savez(npz_path,XP=x_protein, XR=x_rna, Y=y)
    
    if isPrint :
        print("Protein feature : {}".format(x_protein.shape))
        print("RNA feature     : {}".format(x_rna.shape))
        print("Labels          : {}".format(y.shape))
        print("Saved path      : {}".format(npz_path))
    
    # x_protein : 이차원 배열. 각 원소는 1차원 배열이고 protein value에 대해 feature를 추출한 것을 최소최대정규화 한 것이다.
    # x_protein eg. [ [0.51851852 0.03703704 0.         ... 0.         0.         0.        ], [0.74916388 0.09364548 0.01672241 ... 0.         0.         0.        ], ..., ] 각각의 원소(배열)의 길이는 모두 399이다. 왜??
    # [모든 원소의 길이가 399인 이유] protein 서열의 길이와 상관없이, 추출하려는 feature 항목의 개수는 동일하게 399이기 때문.
    # 그래서 protein 서열 길이가 짧으면 feature에 체크되는 항목 개수가 적을 것이고, 길이가 길면, 항목 개수가 많을 것이다.
    
    # 그래서 x_protein의 행은 각각의 protein 서열이고, 세로는, 각각의 feature을 의미한다.
    return x_protein, x_rna, y

def preprocess_and_savez_NPInter():
    X, Y = read_NPInter_pairSeq()
    XP, XR, Y = preprocess_feature(X, Y, NPZ_PATH["NPInter"])
    
def preprocess_and_savez_RPI(size):
    X, Y = read_RPI_pairSeq(size)
    XP, XR, Y = preprocess_feature(X, Y, NPZ_PATH["RPI"][size])

if __name__ == "__main__":
    print("Feature Preprocessing")
    preprocess_and_savez_NPInter()
    preprocess_and_savez_RPI(1807)
    preprocess_and_savez_RPI(2241)
    preprocess_and_savez_RPI(369)
    preprocess_and_savez_RPI(488)
    
    
    
    