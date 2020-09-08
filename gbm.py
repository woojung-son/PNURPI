#!/usr/bin/env python
# coding: utf-8

# In[6]:


from hyperparams import *
from rawdata_preprocessing import *

import Bio
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import mglearn


KFOLD_TIME = 5

feature_names = ['A', 'AA', 'AAA', 'AAB', 'AAC', 'AAD', 'AAE', 'AAF', 'AAG', 'AB', 'ABA', 'ABB', 'ABC', 'ABD', 'ABE', 'ABF', 'ABG', 'AC', 'ACA', 'ACB', 'ACC', 'ACD', 'ACE', 'ACF', 'ACG', 'AD', 'ADA', 'ADB', 'ADC', 'ADD', 'ADE', 'ADF', 'ADG', 'AE', 'AEA', 'AEB', 'AEC', 'AED', 'AEE', 'AEF', 'AEG', 'AF', 'AFA', 'AFB', 'AFC', 'AFD', 'AFE', 'AFF', 'AFG', 'AG', 'AGA', 'AGB', 'AGC', 'AGD', 'AGE', 'AGF', 'AGG', 'B', 'BA', 'BAA', 'BAB', 'BAC', 'BAD', 'BAE', 'BAF', 'BAG', 'BB', 'BBA', 'BBB', 'BBC', 'BBD', 'BBE', 'BBF', 'BBG', 'BC', 'BCA', 'BCB', 'BCC', 'BCD', 'BCE', 'BCF', 'BCG', 'BD', 'BDA', 'BDB', 'BDC', 'BDD', 'BDE', 'BDF', 'BDG', 'BE', 'BEA', 'BEB', 'BEC', 'BED', 'BEE', 'BEF', 'BEG', 'BF', 'BFA', 'BFB', 'BFC', 'BFD', 'BFE', 'BFF', 'BFG', 'BG', 'BGA', 'BGB', 'BGC', 'BGD', 'BGE', 'BGF', 'BGG', 'C', 'CA', 'CAA', 'CAB', 'CAC', 'CAD', 'CAE', 'CAF', 'CAG', 'CB', 'CBA', 'CBB', 'CBC', 'CBD', 'CBE', 'CBF', 'CBG', 'CC', 'CCA', 'CCB', 'CCC', 'CCD', 'CCE', 'CCF', 'CCG', 'CD', 'CDA', 'CDB', 'CDC', 'CDD', 'CDE', 'CDF', 'CDG', 'CE', 'CEA', 'CEB', 'CEC', 'CED', 'CEE', 'CEF', 'CEG', 'CF', 'CFA', 'CFB', 'CFC', 'CFD', 'CFE', 'CFF', 'CFG', 'CG', 'CGA', 'CGB', 'CGC', 'CGD', 'CGE', 'CGF', 'CGG', 'D', 'DA', 'DAA', 'DAB', 'DAC', 'DAD', 'DAE', 'DAF', 'DAG', 'DB', 'DBA', 'DBB', 'DBC', 'DBD', 'DBE', 'DBF', 'DBG', 'DC', 'DCA', 'DCB', 'DCC', 'DCD', 'DCE', 'DCF', 'DCG', 'DD', 'DDA', 'DDB', 'DDC', 'DDD', 'DDE', 'DDF', 'DDG', 'DE', 'DEA', 'DEB', 'DEC', 'DED', 'DEE', 'DEF', 'DEG', 'DF', 'DFA', 'DFB', 'DFC', 'DFD', 'DFE', 'DFF', 'DFG', 'DG', 'DGA', 'DGB', 'DGC', 'DGD', 'DGE', 'DGF', 'DGG', 'E', 'EA', 'EAA', 'EAB', 'EAC', 'EAD', 'EAE', 'EAF', 'EAG', 'EB', 'EBA', 'EBB', 'EBC', 'EBD', 'EBE', 'EBF', 'EBG', 'EC', 'ECA', 'ECB', 'ECC', 'ECD', 'ECE', 'ECF', 'ECG', 'ED', 'EDA', 'EDB', 'EDC', 'EDD', 'EDE', 'EDF', 'EDG', 'EE', 'EEA', 'EEB', 'EEC', 'EED', 'EEE', 'EEF', 'EEG', 'EF', 'EFA', 'EFB', 'EFC', 'EFD', 'EFE', 'EFF', 'EFG', 'EG', 'EGA', 'EGB', 'EGC', 'EGD', 'EGE', 'EGF', 'EGG', 'F', 'FA', 'FAA', 'FAB', 'FAC', 'FAD', 'FAE', 'FAF', 'FAG', 'FB', 'FBA', 'FBB', 'FBC', 'FBD', 'FBE', 'FBF', 'FBG', 'FC', 'FCA', 'FCB', 'FCC', 'FCD', 'FCE', 'FCF', 'FCG', 'FD', 'FDA', 'FDB', 'FDC', 'FDD', 'FDE', 'FDF', 'FDG', 'FE', 'FEA', 'FEB', 'FEC', 'FED', 'FEE', 'FEF', 'FEG', 'FF', 'FFA', 'FFB', 'FFC', 'FFD', 'FFE', 'FFF', 'FFG', 'FG', 'FGA', 'FGB', 'FGC', 'FGD', 'FGE', 'FGF', 'FGG', 'G', 'GA', 'GAA', 'GAB', 'GAC', 'GAD', 'GAE', 'GAF', 'GAG', 'GB', 'GBA', 'GBB', 'GBC', 'GBD', 'GBE', 'GBF', 'GBG', 'GC', 'GCA', 'GCB', 'GCC', 'GCD', 'GCE', 'GCF', 'GCG', 'GD', 'GDA', 'GDB', 'GDC', 'GDD', 'GDE', 'GDF', 'GDG', 'GE', 'GEA', 'GEB', 'GEC', 'GED', 'GEE', 'GEF', 'GEG', 'GF', 'GFA', 'GFB', 'GFC', 'GFD', 'GFE', 'GFF', 'GFG', 'GG', 'GGA', 'GGB', 'GGC', 'GGD', 'GGE', 'GGF', 'GGG']
r_feature_names = ['A', 'AA', 'AAA', 'AAAA', 'AAAC', 'AAAG', 'AAAU', 'AAC', 'AACA', 'AACC', 'AACG', 'AACU', 'AAG', 'AAGA', 'AAGC', 'AAGG', 'AAGU', 'AAU', 'AAUA', 'AAUC', 'AAUG', 'AAUU', 'AC', 'ACA', 'ACAA', 'ACAC', 'ACAG', 'ACAU', 'ACC', 'ACCA', 'ACCC', 'ACCG', 'ACCU', 'ACG', 'ACGA', 'ACGC', 'ACGG', 'ACGU', 'ACU', 'ACUA', 'ACUC', 'ACUG', 'ACUU', 'AG', 'AGA', 'AGAA', 'AGAC', 'AGAG', 'AGAU', 'AGC', 'AGCA', 'AGCC', 'AGCG', 'AGCU', 'AGG', 'AGGA', 'AGGC', 'AGGG', 'AGGU', 'AGU', 'AGUA', 'AGUC', 'AGUG', 'AGUU', 'AU', 'AUA', 'AUAA', 'AUAC', 'AUAG', 'AUAU', 'AUC', 'AUCA', 'AUCC', 'AUCG', 'AUCU', 'AUG', 'AUGA', 'AUGC', 'AUGG', 'AUGU', 'AUU', 'AUUA', 'AUUC', 'AUUG', 'AUUU', 'C', 'CA', 'CAA', 'CAAA', 'CAAC', 'CAAG', 'CAAU', 'CAC', 'CACA', 'CACC', 'CACG', 'CACU', 'CAG', 'CAGA', 'CAGC', 'CAGG', 'CAGU', 'CAU', 'CAUA', 'CAUC', 'CAUG', 'CAUU', 'CC', 'CCA', 'CCAA', 'CCAC', 'CCAG', 'CCAU', 'CCC', 'CCCA', 'CCCC', 'CCCG', 'CCCU', 'CCG', 'CCGA', 'CCGC', 'CCGG', 'CCGU', 'CCU', 'CCUA', 'CCUC', 'CCUG', 'CCUU', 'CG', 'CGA', 'CGAA', 'CGAC', 'CGAG', 'CGAU', 'CGC', 'CGCA', 'CGCC', 'CGCG', 'CGCU', 'CGG', 'CGGA', 'CGGC', 'CGGG', 'CGGU', 'CGU', 'CGUA', 'CGUC', 'CGUG', 'CGUU', 'CU', 'CUA', 'CUAA', 'CUAC', 'CUAG', 'CUAU', 'CUC', 'CUCA', 'CUCC', 'CUCG', 'CUCU', 'CUG', 'CUGA', 'CUGC', 'CUGG', 'CUGU', 'CUU', 'CUUA', 'CUUC', 'CUUG', 'CUUU', 'G', 'GA', 'GAA', 'GAAA', 'GAAC', 'GAAG', 'GAAU', 'GAC', 'GACA', 'GACC', 'GACG', 'GACU', 'GAG', 'GAGA', 'GAGC', 'GAGG', 'GAGU', 'GAU', 'GAUA', 'GAUC', 'GAUG', 'GAUU', 'GC', 'GCA', 'GCAA', 'GCAC', 'GCAG', 'GCAU', 'GCC', 'GCCA', 'GCCC', 'GCCG', 'GCCU', 'GCG', 'GCGA', 'GCGC', 'GCGG', 'GCGU', 'GCU', 'GCUA', 'GCUC', 'GCUG', 'GCUU', 'GG', 'GGA', 'GGAA', 'GGAC', 'GGAG', 'GGAU', 'GGC', 'GGCA', 'GGCC', 'GGCG', 'GGCU', 'GGG', 'GGGA', 'GGGC', 'GGGG', 'GGGU', 'GGU', 'GGUA', 'GGUC', 'GGUG', 'GGUU', 'GU', 'GUA', 'GUAA', 'GUAC', 'GUAG', 'GUAU', 'GUC', 'GUCA', 'GUCC', 'GUCG', 'GUCU', 'GUG', 'GUGA', 'GUGC', 'GUGG', 'GUGU', 'GUU', 'GUUA', 'GUUC', 'GUUG', 'GUUU', 'U', 'UA', 'UAA', 'UAAA', 'UAAC', 'UAAG', 'UAAU', 'UAC', 'UACA', 'UACC', 'UACG', 'UACU', 'UAG', 'UAGA', 'UAGC', 'UAGG', 'UAGU', 'UAU', 'UAUA', 'UAUC', 'UAUG', 'UAUU', 'UC', 'UCA', 'UCAA', 'UCAC', 'UCAG', 'UCAU', 'UCC', 'UCCA', 'UCCC', 'UCCG', 'UCCU', 'UCG', 'UCGA', 'UCGC', 'UCGG', 'UCGU', 'UCU', 'UCUA', 'UCUC', 'UCUG', 'UCUU', 'UG', 'UGA', 'UGAA', 'UGAC', 'UGAG', 'UGAU', 'UGC', 'UGCA', 'UGCC', 'UGCG', 'UGCU', 'UGG', 'UGGA', 'UGGC', 'UGGG', 'UGGU', 'UGU', 'UGUA', 'UGUC', 'UGUG', 'UGUU', 'UU', 'UUA', 'UUAA', 'UUAC', 'UUAG', 'UUAU', 'UUC', 'UUCA', 'UUCC', 'UUCG', 'UUCU', 'UUG', 'UUGA', 'UUGC', 'UUGG', 'UUGU', 'UUU', 'UUUA', 'UUUC', 'UUUG', 'UUUU']


def classify(npz_path) :
    print("Dataset : ", npz_path)
    mydata = np.load(npz_path)
    XP = mydata['XP']
    XR = mydata['XR']
    Y = mydata['Y']

    gbrt = GradientBoostingClassifier(random_state = 0)
    gbrt.fit(XP, Y)
    print("훈련 세트 정확도 : {:.3f}".format(gbrt.score(XP, Y)))
    #파라미터 조정해서 오버피팅 방지하도록 조정
    combined_pd = pd.DataFrame(data= np.c_[np.c_[XP, XR], Y], columns= feature_names + r_feature_names + ['target'])

    features = list(combined_pd.columns[:-1])
    X = combined_pd[features]
    y = combined_pd['target']

    score_list = cross_val_score(gbrt, X, y, cv=KFOLD_TIME)
    result = list(map(lambda x: '{score:.2f}'.format(score=x), score_list))
    return result

def classify_and_print_NPInter():
    print("=======================================================")
    result = classify(NPZ_PATH["NPInter"])
    print("K_fold with", KFOLD_TIME, "epoch : ", result)
    
def classify_and_print_RPI(size):
    print("=======================================================")
    result = classify(NPZ_PATH["RPI"][size])
    print(result)

if __name__ == "__main__":
    print("Classification is about to start ... ")
    classify_and_print_NPInter()
    classify_and_print_RPI(1807)
    classify_and_print_RPI(2241)
    classify_and_print_RPI(369)
    classify_and_print_RPI(488)


# In[ ]:




