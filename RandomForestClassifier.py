
from hyperparams import *
from rawdata_preprocessing import *
#from RandomForestClassifier import *

import Bio
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

def RF_Classifying(X, y, KFOLD_TIME) :
    rf = RandomForestClassifier(random_state=1)
    score_list = cross_val_score(rf, X, y, cv=KFOLD_TIME)
    result = list(map(lambda x: '{score:.2f}'.format(score=x), score_list))
    return result
