
#!/usr/bin/python3 
from hyperparams import *
from rawstruct_preprocessing_debug import *
from rawdata_preprocessing import read_RPI_pairSeq, read_NPInter_pairSeq
from copy import deepcopy
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pylab as plt
import sys
from sklearn.preprocessing import StandardScaler
import math
import string
from functools import reduce

import numpy as np


# encoder for protein sequence
class ProEncoder:
    elements = 'AIYHRDC'
    structs = 'hec'

    element_number = 7
    # number of structure kind
    struct_kind = 3

    # clusters: {A,G,V}, {I,L,F,P}, {Y,M,T,S}, {H,N,Q,W}, {R,K}, {D,E}, {C}
    pro_intab = 'AGVILFPYMTSHNQWRKDEC'
    pro_outtab = 'AAAIIIIYYYYHHHHRRDDC'

    def __init__(self, WINDOW_P_UPLIMIT, WINDOW_P_STRUCT_UPLIMIT, CODING_FREQUENCY, VECTOR_REPETITION_CNN,
                 TRUNCATION_LEN=None, PERIOD_EXTENDED=None):
        #WINDOW_P_UPLIMIT : protein feature를 최대 몇자리까지 쓸것인가를 저장한 상수. 3
        #WINDOW_P_STRUCT_UPLIMIT : struct 정보의 protein feature를 최대 몇자리까지 쓸것인가를 저장한 상수. 3
        #CODING_FREQUENCY : 전역상수. True.
        #VECTOR_REPETITION_CNN : 전역상수. 1.
        
        self.WINDOW_P_UPLIMIT = WINDOW_P_UPLIMIT
        self.WINDOW_P_STRUCT_UPLIMIT = WINDOW_P_STRUCT_UPLIMIT
        self.CODING_FREQUENCY = CODING_FREQUENCY
        self.VECTOR_REPETITION_CNN = VECTOR_REPETITION_CNN

        self.TRUNCATION_LEN = TRUNCATION_LEN
        self.PERIOD_EXTENDED = PERIOD_EXTENDED

        # list and position map for k_mer
        k_mers = ['']
        self.k_mer_list = []
        self.k_mer_map = {}
        for T in range(self.WINDOW_P_UPLIMIT): # 3
            temp_list = []
            for k_mer in k_mers:
                for x in self.elements:# AIYHRDC 
                    temp_list.append(k_mer + x)
            k_mers = temp_list
            self.k_mer_list += temp_list
        for i in range(len(self.k_mer_list)):
            self.k_mer_map[self.k_mer_list[i]] = i

        # list and position map for k_mer structure
        k_mers = ['']
        self.k_mer_struct_list = []
        self.k_mer_struct_map = {}
        for T in range(self.WINDOW_P_STRUCT_UPLIMIT):
            temp_list = []
            for k_mer in k_mers: 
                for s in self.structs:
                    temp_list.append(k_mer + s)
            k_mers = temp_list
            self.k_mer_struct_list += temp_list
        for i in range(len(self.k_mer_struct_list)):
            self.k_mer_struct_map[self.k_mer_struct_list[i]] = i

        # table for amino acid clusters
        self.transtable = str.maketrans(self.pro_intab, self.pro_outtab)
        
        #k_mer_map : feature들을 key값으로, 그것의 index를 value값으로 가지는 딕셔너리
        # k_mer_map 0~6 : 한 자리 알파벳으로 이루어진 원소
        # k_mer_map 7~55 : 두 자리 알파벳으로 이루어진 원소
        # k_mer_map 56~398 : 세 자리 알파벳으로 이루어진 원소
        
        #k_mer_list : feature들이 sorting되어 있는 리스트

        # print(len(self.k_mer_list))
        # print(self.k_mer_list)
        #print('self.k_mer_map : {}'.format(self.k_mer_map))
        # print(len(self.k_mer_struct_list))
        # print(self.k_mer_struct_list)


    def encode_conjoint(self, seq): 
        # sequence에서 각각의 feature들이 포함되는 횟수를 세서 정규화시킴. improved CTF. 우리 프로젝트랑 똑같음.
        # 정규화시키는 방법이 다름. min_max 정규화가 아니고, value를 최대값으로 나눔.
        
        seq = seq.translate(self.transtable) # seq는 문자열 # 'AGVILFPYMTSHNQWRKDEC' -> 'AAAIIIIYYYYHHHHRRDDC' 이렇게 바꿈.
        #print('seq before join : {}'.format(seq)) # 이건 AIYHRDC로만 이루어졌나 아닌가 체크하는 로직인 듯
        #seq = ''.join([x for x in seq if x in self.elements]) # seq는 문자열.
        #print('seq after_ join : {}'.format(seq))
        seq_len = len(seq)
        if seq_len == 0:
            return 'Error'
        result = []
        offset = 0
        for K in range(1, self.WINDOW_P_UPLIMIT + 1): # range(1, 4)
            # K는 feature의 길이임. 
            
            vec = [0.0] * (self.element_number ** K) 
            # vec배열을 7**K 개의 0.0 (float)가 담긴 배열로 초기화
            # element_number : 7
            
            counter = seq_len - K + 1
            for i in range(seq_len - K + 1): # K=1일 때는 sequence의 length만큼 순회. K=2일 때는 sequence의 length - 1만큼 순회. K=일때는 ...
                k_mer = seq[i:i + K] # feature를 순회하면서 K 길이의 문자열을 추출한거.
                vec[self.k_mer_map[k_mer] - offset] += 1 # vec 리스트에서 k_mer의 인덱스에 해당하는 자리에 카운트를 1 올림.
            vec = np.array(vec)
            offset += vec.size # K=1 일 때 vec.size = 7, K=2일 때 vec.size = 49, K=3일 때 vec.size = 343
            #print('self.k_mer_map[k_mer] : {}'.format(self.k_mer_map[k_mer]))
            #print('vec : {0} - vec.size : {1}'.format(vec, vec.size))
            if self.CODING_FREQUENCY:
                vec = vec / vec.max()
            result += list(vec)
            #print('len of result : {}'.format(len(result)))
        #print('result : {}'.format(result))
        
        # result 0~6 : 한 자리 알파벳으로 이루어진 원소
        # result 7~55 : 두 자리 알파벳으로 이루어진 원소
        # result 56~398 : 세 자리 알파벳으로 이루어진 원소
        return np.array(result)

    def encode_conjoint_struct(self, seq, struct):
        # seq length와 struct length는 같음. 헐.

        
        seq = seq.translate(self.transtable) # seq는 문자열 # 'AGVILFPYMTSHNQWRKDEC' -> 'AAAIIIIYYYYHHHHRRDDC' 이렇게 바꿈.
        seq_temp = []
        struct_temp = []
        for i in range(len(seq)):     
            if seq[i] in self.elements:
                # AIYHRDC 의 원소가 AIYHRDC안에 있으면, 0~len(seq)-1 의 모든 인덱스에 대해 translate된 seq[i]와 원본 struct[i]를 배열로 보관함.
                
                seq_temp.append(seq[i])
                struct_temp.append(struct[i])
        seq = ''.join(seq_temp) # 여기의 seq는 translate된 seq와 같음. (그냥 검증로직인듯)
        struct = ''.join(struct_temp) # 그냥 원본 struct와 같음.
        seq_len = len(seq)
        if seq_len == 0:
            return 'Error'

        
        # encode_conjoint의 sequence 인코딩 방식과 정확하게 동일함.
        result_seq = []
        offset_seq = 0
        for K in range(1, self.WINDOW_P_UPLIMIT + 1):
            vec_seq = [0.0] * (self.element_number ** K)
            counter = seq_len - K + 1
            for i in range(seq_len - K + 1):
                k_mer = seq[i:i + K]
                vec_seq[self.k_mer_map[k_mer] - offset_seq] += 1 # vec 리스트에서 k_mer의 인덱스에 해당하는 자리에 카운트를 1 올림.
            vec_seq = np.array(vec_seq)
            offset_seq += vec_seq.size
            if self.CODING_FREQUENCY:
                vec_seq = vec_seq / vec_seq.max()
            result_seq += list(vec_seq)


        result_struct = []
        offset_struct = 0
        for K in range(1, self.WINDOW_P_STRUCT_UPLIMIT + 1):
            vec_struct = [0.0] * (self.struct_kind ** K)
            # vec배열을 3^K 개의 0.0 (float)가 담긴 배열로 초기화
            # element_number : 3
            
            counter = seq_len - K + 1
            for i in range(seq_len - K + 1):
                k_mer_struct = struct[i:i + K]
                vec_struct[self.k_mer_struct_map[k_mer_struct] - offset_struct] += 1
            vec_struct = np.array(vec_struct)
            offset_struct += vec_struct.size
            if self.CODING_FREQUENCY:
                vec_struct = vec_struct / vec_struct.max()
            result_struct += list(vec_struct)
            
        # sequence를 정규화한 배열과 struct를 정규화한 배열을 concatenate시킴.
        # result_seq len : 399
        # result_struct len : 39 -> 3 + 9 + 27. feature의 알파벳 개수가 3개여서 그럼.
        # 결과 : 438 
        return np.array(result_seq + result_struct)

    def encode_conjoint_cnn(self, seq):
        result_t = self.encode_conjoint(seq)
        result = np.array([[x] * self.VECTOR_REPETITION_CNN for x in result_t])
        return result

    def encode_conjoint_struct_cnn(self, seq, struct):
        result_t = self.encode_conjoint_struct(seq, struct)
        result = np.array([[x] * self.VECTOR_REPETITION_CNN for x in result_t])
        return result



# encoder for RNA sequence
class RNAEncoder:
    elements = 'AUCG'
    structs = '.('

    element_number = 4
    struct_kind = 2

    def __init__(self, WINDOW_R_UPLIMIT, WINDOW_R_STRUCT_UPLIMIT, CODING_FREQUENCY, VECTOR_REPETITION_CNN,
                 TRUNCATION_LEN=None, PERIOD_EXTENDED=None):

        self.WINDOW_R_UPLIMIT = WINDOW_R_UPLIMIT
        self.WINDOW_R_STRUCT_UPLIMIT = WINDOW_R_STRUCT_UPLIMIT
        self.CODING_FREQUENCY = CODING_FREQUENCY
        self.VECTOR_REPETITION_CNN = VECTOR_REPETITION_CNN

        self.TRUNCATION_LEN = TRUNCATION_LEN
        self.PERIOD_EXTENDED = PERIOD_EXTENDED

        # list and position map for k_mer
        k_mers = ['']
        self.k_mer_list = []
        self.k_mer_map = {}
        for T in range(self.WINDOW_R_UPLIMIT):
            temp_list = []
            for k_mer in k_mers:
                for x in self.elements:
                    temp_list.append(k_mer + x)
            k_mers = temp_list
            self.k_mer_list += temp_list
        for i in range(len(self.k_mer_list)):
            self.k_mer_map[self.k_mer_list[i]] = i

        # list and position map for k_mer structure
        k_mers = ['']
        self.k_mer_struct_list = []
        self.k_mer_struct_map = {}
        for T in range(self.WINDOW_R_STRUCT_UPLIMIT):
            temp_list = []
            for k_mer in k_mers:
                for s in self.structs:
                    temp_list.append(k_mer + s)
            k_mers = temp_list
            self.k_mer_struct_list += temp_list
        for i in range(len(self.k_mer_struct_list)):
            self.k_mer_struct_map[self.k_mer_struct_list[i]] = i

        # print(len(self.k_mer_list))
        # print(self.k_mer_list)
        # print(len(self.k_mer_struct_list))
        # print(self.k_mer_struct_list)

    def encode_conjoint(self, seq):
        seq = seq.replace('T', 'U')
        seq = ''.join([x for x in seq if x in self.elements])
        seq_len = len(seq)
        if seq_len == 0:
            return 'Error'
        result = []
        offset = 0
        for K in range(1, self.WINDOW_R_UPLIMIT + 1):
            vec = [0.0] * (self.element_number ** K)
            counter = seq_len - K + 1
            for i in range(seq_len - K + 1):
                k_mer = seq[i:i + K]
                vec[self.k_mer_map[k_mer] - offset] += 1
            vec = np.array(vec)
            offset += vec.size
            if self.CODING_FREQUENCY:
                vec = vec / vec.max()
            result += list(vec)
        return np.array(result)

    def encode_conjoint_struct(self, seq, struct):
        seq = seq.replace('T', 'U')
        struct = struct.replace(')', '(')
        seq_temp = []
        struct_temp = []
        for i in range(len(seq)):
            if seq[i] in self.elements:
                seq_temp.append(seq[i])
                struct_temp.append(struct[i])
        seq = ''.join(seq_temp)
        struct = ''.join(struct_temp)
        seq_len = len(seq)
        if seq_len == 0:
            return 'Error'

        result_seq = []
        offset_seq = 0
        for K in range(1, self.WINDOW_R_UPLIMIT + 1):
            vec_seq = [0.0] * (self.element_number ** K)
            counter = seq_len - K + 1
            for i in range(seq_len - K + 1):
                k_mer = seq[i:i + K]
                vec_seq[self.k_mer_map[k_mer] - offset_seq] += 1
            vec_seq = np.array(vec_seq)
            offset_seq += vec_seq.size
            if self.CODING_FREQUENCY:
                vec_seq = vec_seq / vec_seq.max()
            result_seq += list(vec_seq)


        result_struct = []
        offset_struct = 0
        for K in range(1, self.WINDOW_R_STRUCT_UPLIMIT + 1):
            vec_struct = [0.0] * (self.struct_kind ** K)
            counter = seq_len - K + 1
            for i in range(seq_len - K + 1):
                k_mer_struct = struct[i:i + K]
                vec_struct[self.k_mer_struct_map[k_mer_struct] - offset_struct] += 1
            vec_struct = np.array(vec_struct)
            offset_struct += vec_struct.size
            if self.CODING_FREQUENCY:
                vec_struct = vec_struct / vec_struct.max()
            result_struct += list(vec_struct)
        return np.array(result_seq + result_struct)

    def encode_conjoint_cnn(self, seq):
        result_t = self.encode_conjoint(seq)
        result = np.array([[x] * self.VECTOR_REPETITION_CNN for x in result_t])
        return result

    def encode_conjoint_struct_cnn(self, seq, struct):
        result_t = self.encode_conjoint_struct(seq, struct)
        result = np.array([[x] * self.VECTOR_REPETITION_CNN for x in result_t])
        return result


def standardization(X):
    # https://datascienceschool.net/view-notebook/f43be7d6515b48c0beb909826993c856/
    # StandardScalar : 평균이 0과 표준편차가 1이 되도록 변환.
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    return X, scaler

def coding_pairs(pairs, pro_seqs, rna_seqs, pro_structs, rna_structs, PE, RE, kind):
    # pair (p_sequence, r_sequence)에서 각 feature를 순회하면서 feature들의 value를 추출하고, 그것을 정규화시킨 것을 배열로 만듬.
    # p_sequence에 해당하는 p_struct를 인코딩해서 배열로 만들고, p_sequence의 값과 concatenate시킴.
    # kind = 1 (positive) or 0 (negative)인 Flag
     
    samples = []
    for pr in pairs:
        #print('kind : {0} - pair : {1} - struct : {2}'.format(kind, pr, pr[0] in pro_seqs and pr[1] in rna_seqs and pr[0] in pro_structs and pr[1] in rna_structs))
        if pr[0] in pro_seqs and pr[1] in rna_seqs and pr[0] in pro_structs and pr[1] in rna_structs:
            # 이 if 문은 결측치를 처리하기 위함임. 결측치가 포함된 pair를 단순히 제외시킨다.
            # pr[0] in pro_structs 라는게, pro_structs 딕셔너리의 key 값중 pr[0]이 포함되어있는지 보는것인 듯.
            p_seq = pro_seqs[pr[0]]  # protein sequence
            r_seq = rna_seqs[pr[1]]  # rna sequence
            p_struct = pro_structs[pr[0]]  # protein structure
            r_struct = rna_structs[pr[1]]  # rna structure

            #p_conjoint = PE.encode_conjoint(p_seq) # protein sequence를 인코딩함. feature마다 count된 value를 최대값으로 나눈 정규화 사용. 그외 동일
            #r_conjoint = RE.encode_conjoint(r_seq)
            print('woojung3')
            p_conjoint_struct = PE.encode_conjoint_struct(p_seq, p_struct)
            # struct 파일도 sequence와 완전 동일한 방법으로 인코딩. result인, '정규화된 값으로 구성된 배열'들을 concatenate시켜서 결과로 리턴.
        
            r_conjoint_struct = RE.encode_conjoint_struct(r_seq, r_struct)

            if p_conjoint is 'Error':
                print('Skip {} in pair {} according to conjoint coding process.'.format(pr[0], pr))
            elif r_conjoint is 'Error':
                print('Skip {} in pair {} according to conjoint coding process.'.format(pr[1], pr))
            elif p_conjoint_struct is 'Error':
                print('Skip {} in pair {} according to conjoint_struct coding process.'.format(pr[0], pr))
            elif r_conjoint_struct is 'Error':
                print('Skip {} in pair {} according to conjoint_struct coding process.'.format(pr[1], pr))

            else:
                samples.append([[p_conjoint, r_conjoint],
                                [p_conjoint_struct, r_conjoint_struct],
                                kind])
        else:
            print('Skip pair {} according to sequence dictionary.'.format(pr))
            
    # samples (4차원 배열) : "[[p_conjoint, r_conjoint],[p_conjoint_struct, r_conjoint_struct], kind]" 이게 원소로 들어가있음.
    # p_conjoint, p_conjoint_struct는 feature들의 value가 정규화되어 들어가있는 1차원 배열.
    return samples

def pre_process_data(samples, samples_pred=None):
    # parameter samples는 아래와 같이 생겼음.
    # [ [[p1_conjoint, r1_conjoint],[p1_conjoint_struct, r1_conjoint_struct],kind], 
    #   [[p2_conjoint, r2_conjoint],[p2_conjoint_struct, r2_conjoint_struct],kind],
    #   [[p3_conjoint, r3_conjoint],[p3_conjoint_struct, r3_conjoint_struct],kind],
    #    ...
    #   [[pN_conjoint, rN_conjoint],[pN_conjoint_struct, rN_conjoint_struct],kind]
    # ]
    
    # np.random.shuffle(samples)
    #print('samples : {}'.format(samples))

    p_conjoint = np.array([x[0][0] for x in samples]) # x[?][0][0] : p_conjoint
    r_conjoint = np.array([x[0][1] for x in samples]) # x[?][0][1] : r_conjoint
    p_conjoint_struct = np.array([x[1][0] for x in samples]) # x[?][1][0] : p_conjoint_struct
    r_conjoint_struct = np.array([x[1][1] for x in samples]) # x[?][1][1] : r_conjoint_struct
    y_samples = np.array([x[2] for x in samples]) # x[2] : kind
    # p_conjoint (2차원 배열) (이 시점에서의 p_conjoint) : [p1_conjoint, p2_conjoint, p3_conjoint ... ]
    # r_conjoint (2차원 배열) (이 시점에서의 r_conjoint) : [r1_conjoint, r2_conjoint, r3_conjoint ... ]
    # p_conjoint_struct (2차원 배열) (이 시점에서의 p_conjoint_struct) : [p1_conjoint_struct, p2_conjoint_struct, ... ]
    # r_conjoint_struct (2차원 배열) (이 시점에서의 r_conjoint_struct) : [r1_conjoint_struct, r2_conjoint_struct, ... ]
    
    # p_conjoint length : 488
    # p_conjoint[0] length : 343 

    #print('before standardization : {}'.format(p_conjoint)) 
    p_conjoint, scaler_p = standardization(p_conjoint)
    #print('after standardization - p_conjoint : {0} - scaler_p : {1}'.format(p_conjoint, scaler_p))
    
    r_conjoint, scaler_r = standardization(r_conjoint)
    p_conjoint_struct, scaler_p_struct = standardization(p_conjoint_struct)
    r_conjoint_struct, scaler_r_struct = standardization(r_conjoint_struct)

    #print('p_conjoint : {0} - len of p_conjoint : {1} - len of p_conjoint[0] : {2}'.format(p_conjoint, len(p_conjoint), len(p_conjoint[0])))
    p_conjoint_cnn = np.array([list(map(lambda e: [e] * VECTOR_REPETITION_CNN, x)) for x in p_conjoint])
    # map과 람다 함수 : map(function, iterator) -> iterator (e.g. list, tuple, ... )의 각 요소를 function의 파라미터로 넣어서 실행시킨다.
    # p_conjoint의 각 인자와 VECTOR_REPETITION_CNN를 곱함.
    #print('p_conjoint_cnn : {}'.format(p_conjoint_cnn))
    
    r_conjoint_cnn = np.array([list(map(lambda e: [e] * VECTOR_REPETITION_CNN, x)) for x in r_conjoint])
    p_conjoint_struct_cnn = np.array([list(map(lambda e: [e] * VECTOR_REPETITION_CNN, x)) for x in p_conjoint_struct])
    r_conjoint_struct_cnn = np.array([list(map(lambda e: [e] * VECTOR_REPETITION_CNN, x)) for x in r_conjoint_struct])

    p_ctf_len = 7 ** WINDOW_P_UPLIMIT # WINDOW_P_UPLIMIT : 3, 7 ** WINDOW_P_UPLIMI : 343
    r_ctf_len = 4 ** WINDOW_R_UPLIMIT # WINDOW_R_UPLIMIT : 4, 4 ** WINDOW_R_UPLIMIT : 256
    p_conjoint_previous = np.array([x[-p_ctf_len:] for x in p_conjoint]) 
    # 각 p_sequence의 정규화 배열에 대해 인덱스가 뒤에서부터 343번째 까지인 것만 배열로 만듬. -> 세자리 알파벳인 feature의 정규값 원소만 뽑겠다!
    # 파이썬 배열 인덱싱 - 마이너스가 붙으면 뒤에서부터 탐색. 
    # p_sequence 배열의 인덱스의 의미 !!
    # p_sequence 0~6 : 한 자리 알파벳으로 이루어진 원소
    # p_sequence 7~55 : 두 자리 알파벳으로 이루어진 원소
    # p_sequence 56~398 : 세 자리 알파벳으로 이루어진 원소
    
    #print('p_conjoint_previous : {0} - p_ctf_len : {1} - len of p_conjoint_previous[0] : {2}'.format(p_conjoint_previous, p_ctf_len, len(p_conjoint_previous[0])))
    
    r_conjoint_previous = np.array([x[-r_ctf_len:] for x in r_conjoint])
    '''
    X_samples = [[p_conjoint, r_conjoint],
                 [p_conjoint_struct, r_conjoint_struct],
                 [p_conjoint_cnn, r_conjoint_cnn],
                 [p_conjoint_struct_cnn, r_conjoint_struct_cnn],
                 [p_conjoint_previous, r_conjoint_previous]
                 ]
    '''
    X_samples = [p_conjoint_struct, r_conjoint_struct]


    return X_samples, y_samples
