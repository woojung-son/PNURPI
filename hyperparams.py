#!/usr/bin/python3 
import os

CUR_PATH = os.path.dirname(os.path.abspath(__file__)) + "/"
BASE_PATH = CUR_PATH + "/data/"
SEQ_PATH = BASE_PATH + "sequence/"
STR_PATH = BASE_PATH + "structure/"
NPZ_PATH = {
    "NPInter" : CUR_PATH + "npz/NPInter.npz",
    "RPI" : {
        1807 : CUR_PATH + "npz/RPI1807.npz",
        2241 : CUR_PATH + "npz/RPI2241.npz",
        369  : CUR_PATH + "npz/RPI369.npz",
        488  : CUR_PATH + "npz/RPI488.npz"
    }
}
NPZ_PATH_STRUCT = {
    "NPInter" : CUR_PATH + "npz/STRUCT_NPInter.npz",
    "RPI" : {
        1807 : CUR_PATH + "npz/STRUCT_RPI1807.npz",
        2241 : CUR_PATH + "npz/STRUCT_RPI2241.npz",
        369  : CUR_PATH + "npz/STRUCT_RPI369.npz",
        488  : CUR_PATH + "npz/STRUCT_RPI488.npz"
    }
}
Z_NPZ_PATH = {
    "NPInter" : CUR_PATH + "npz/Z_NPInter.npz",
    "RPI" : {
        1807 : CUR_PATH + "npz/Z_RPI1807.npz",
        2241 : CUR_PATH + "npz/Z_RPI2241.npz",
        369  : CUR_PATH + "npz/Z_RPI369.npz",
        488  : CUR_PATH + "npz/Z_RPI488.npz"
    }
}
LOG_NPZ_PATH = {
    "NPInter" : CUR_PATH + "npz/LOG_NPInter.npz",
    "RPI" : {
        1807 : CUR_PATH + "npz/LOG_RPI1807.npz",
        2241 : CUR_PATH + "npz/LOG_RPI2241.npz",
        369  : CUR_PATH + "npz/LOG_RPI369.npz",
        488  : CUR_PATH + "npz/LOG_RPI488.npz"
    }
}
LOG_Z_NPZ_PATH = {
    "NPInter" : CUR_PATH + "npz/LOG_Z_NPInter.npz",
    "RPI" : {
        1807 : CUR_PATH + "npz/LOG_Z_RPI1807.npz",
        2241 : CUR_PATH + "npz/LOG_Z_RPI2241.npz",
        369  : CUR_PATH + "npz/LOG_Z_RPI369.npz",
        488  : CUR_PATH + "npz/LOG_Z_RPI488.npz"
    }
}
LOG_M_NPZ_PATH = {
    "NPInter" : CUR_PATH + "npz/LOG_M_NPInter.npz",
    "RPI" : {
        1807 : CUR_PATH + "npz/LOG_M_RPI1807.npz",
        2241 : CUR_PATH + "npz/LOG_M_RPI2241.npz",
        369  : CUR_PATH + "npz/LOG_M_RPI369.npz",
        488  : CUR_PATH + "npz/LOG_M_RPI488.npz"
    }
}

PAIRS_PATH = {
    "NPInter" : BASE_PATH + "NPInter_pairs.txt",
    "RPI" : {
        1807 : BASE_PATH + "RPI1807_pairs.txt",
        2241 : BASE_PATH + "RPI2241_pairs.txt",
        369  : BASE_PATH + "RPI369_pairs.txt",
        488  : BASE_PATH + "RPI488_pairs.txt"
    }
}
SEQ_PATH = {
    "NPInter" : {
        "RNA"     : SEQ_PATH + "NPinter_rna_seq.fa",
        "Protein" : SEQ_PATH + "NPinter_protein_seq.fa"
    },
    "RPI" : {
        1807 : {
            "RNA"     : SEQ_PATH + "RPI1807_rna_seq.fa",
            "Protein" : SEQ_PATH + "RPI1807_protein_seq.fa"
        },
        2241 : {
            "RNA"     : SEQ_PATH + "RPI2241_rna_seq.fa",
            "Protein" : SEQ_PATH + "RPI2241_protein_seq.fa"
        },
        369  : {
            "RNA"     : SEQ_PATH + "RPI369_rna_seq.fa",
            "Protein" : SEQ_PATH + "RPI369_protein_seq.fa"
        },
        488  : {
            "RNA"     : SEQ_PATH + "RPI488_rna_seq.fa",
            "Protein" : SEQ_PATH + "RPI488_protein_seq.fa"
        }
    }
}
STR_PATH = {
    "NPInter" : {
        "RNA"     : STR_PATH + "NPinter_rna_struct.fa",
        "Protein" : STR_PATH + "NPinter_protein_struct.fa"
    },
    "RPI" : {
        1807 : {
            "RNA"     : STR_PATH + "RPI1807_rna_struct.fa",
            "Protein" : STR_PATH + "RPI1807_protein_struct.fa"
        },
        2241 : {
            "RNA"     : STR_PATH + "RPI2241_rna_struct.fa",
            "Protein" : STR_PATH + "RPI2241_protein_struct.fa"
        },
        369  : {
            "RNA"     : STR_PATH + "RPI369_rna_struct.fa",
            "Protein" : STR_PATH + "RPI369_protein_struct.fa"
        },
        488  : {
            "RNA"     : STR_PATH + "RPI488_rna_struct.fa",
            "Protein" : STR_PATH + "RPI488_protein_struct.fa"
        }
    }
}

# 하이퍼파라미터 덜 찾은 목록 : 
# NPInter SVC, GBC, RFC
# RPI[18007] GBC
# RPI[2241] GBC, LGBM
# RPI[369] GBC
# RPI[488] GBC

PARAM_GRID = {
    "NPInter" : {
        'rfc__max_depth': [7], 'rfc__max_leaf_nodes': [30], 'rfc__min_samples_leaf': [18], 'rfc__min_samples_split': [13], 'rfc__n_estimators': [100],
        'svc__C': [1.0], 'svc__gamma': [0.1], 'svc__kernel': ['linear'],
        'gbc__n_estimators' : [60], 'gbc__max_depth' : [100], 'gbc__min_samples_leaf': [3], 'gbc__min_samples_split' : [10], 'gbc__learning_rate' : [0.1], 'gbc__max_features' : [250],
        'xgb__boosting': ['gblinear'], 'xgb__learning_rate': [0.5], 'xgb__max_depth': [100], 'xgb__num_iterations': [1000],
        #'lgbm__boosting': ['gbdt'], 'lgbm__learning_rate': [0.5], 'lgbm__max_depth': [100], 'lgbm__num_iterations': [1000]
    },
    "RPI" : {
        1807 : {
            'rfc__max_depth': [7], 'rfc__max_leaf_nodes': [30], 'rfc__min_samples_leaf': [18], 'rfc__min_samples_split': [6], 'rfc__n_estimators': [100],
            'svc__C': [1.0], 'svc__gamma': [0.1], 'svc__kernel': ['linear'],
            'gbc__n_estimators' : [60], 'gbc__max_depth' : [100], 'gbc__min_samples_leaf': [3], 'gbc__min_samples_split' : [10], 'gbc__learning_rate' : [0.1], 'gbc__max_features' : [250],
            'xgb__learning_rate': [0.1], 'xgb__num_iterations': [1000], 'xgb__max_depth': [100], 'xgb__boosting': ['gblinear'],
            #'lgbm__boosting': ['gbdt'], 'lgbm__learning_rate': [0.5], 'lgbm__max_depth': [100], 'lgbm__num_iterations': [1000]
            
        },
        2241 : {
            'rfc__max_depth': [7], 'rfc__max_leaf_nodes': [30], 'rfc__min_samples_leaf': [6], 'rfc__min_samples_split': [13], 'rfc__n_estimators': [5],
            'svc__C': [10], 'svc__gamma':[0.01], 'svc__kernel': ['rbf'],
            'gbc__n_estimators' : [60], 'gbc__max_depth' : [100], 'gbc__min_samples_leaf': [3], 'gbc__min_samples_split' : [10], 
            'xgb__learning_rate': [0.075], 'xgb__num_iterations': [1000], 'xgb__max_depth': [100], 'xgb__boosting': ['gblinear'],
            'lgbm__boosting': ['gbdt'], 'lgbm__learning_rate': [0.5], 'lgbm__max_depth': [100], 'lgbm__num_iterations': [1000]
        },
        369  : {
            'rfc__max_depth': [6], 'rfc__max_leaf_nodes': [10], 'rfc__min_samples_leaf': [8], 'rfc__min_samples_split': [20], 'rfc__n_estimators': [30],
            'svc__C': [10], 'svc__gamma': [0.01], 'svc__kernel': ['rbf'],
            #'gbc__n_estimators' : [60], 'gbc__max_depth' : [100], 'gbc__min_samples_leaf': [3], 'gbc__min_samples_split' : [10], 'gbc__learning_rate' : [0.1], 'gbc__max_features' : [250],
            #'xgb__learning_rate': [0.1], 'xgb__num_iterations': [1000], 'xgb__max_depth': [100], 'xgb__boosting': ['gblinear'],
            #'lgbm__boosting': ['dart'], 'lgbm__learning_rate': [0.075], 'lgbm__max_depth': [100], 'lgbm__num_iterations': [1000]
        },
        488  : {
            'rfc__max_depth': [6], 'rfc__max_leaf_nodes': [10], 'rfc__min_samples_leaf': [7], 'rfc__min_samples_split': [13], 'rfc__n_estimators': [125],
            'svc__C': [0.01], 'svc__gamma': [0.01], 'svc__kernel': ['linear'],
            'gbc__n_estimators' : [60], 'gbc__max_depth' : [100], 'gbc__min_samples_leaf': [3], 'gbc__min_samples_split' : [10], 'gbc__learning_rate' : [0.1], 'gbc__max_features' : [250],
            'xgb__learning_rate': [0.075], 'xgb__num_iterations': [1000], 'xgb__max_depth': [100], 'xgb__boosting': ['gblinear'],
            'lgbm__boosting': ['dart'], 'lgbm__learning_rate': [0.01], 'lgbm__max_depth': [100], 'lgbm__num_iterations': [1000]
        }
    }
}

'''
PARAM_GRID = {
    "NPInter" : {
        "RFC" : {'max_depth': [7, 8, 9], 'max_leaf_nodes': [5, 10, 15, 20, 30], 'min_samples_leaf': [15, 18, 21, 24, 30], 'min_samples_split': [6, 8, 10, 13], 'n_estimators': [50, 100, 125]},
        "SVC" : {},
        "GBC" : {},
        "XGB" : {'learning_rate': [0.01, 0.05, 0.075, 0.1, 0.5], 'num_iterations': [1000, 3000, 6000], 'max_depth': [100, 250, 500], 'boosting': ['gblinear', 'gbtree', 'dart']},
        "LGBM" : {'learning_rate': [0.01, 0.05, 0.075, 0.1, 0.5], 'num_iterations': [1000, 3000, 6000], 'max_depth': [100, 250, 500], 'boosting': ['gblinear', 'gbtree', 'dart']}
    },
    "RPI" : {
        1807 : {
            "RFC" : {'max_depth': [7, 8, 9], 'max_leaf_nodes': [5, 10, 15, 20, 30], 'min_samples_leaf': [15, 18, 21, 24, 30], 'min_samples_split': [6, 8, 10, 13], 'n_estimators': [50, 100, 125]},
            "SVC" : {},
            "GBC" : {},
            "XGB" : {'learning_rate': [0.01, 0.05, 0.075, 0.1, 0.5], 'num_iterations': [1000, 3000, 6000], 'max_depth': [100, 250, 500], 'boosting': ['gblinear', 'gbtree', 'dart']},
            "LGBM" : {'learning_rate': [0.01, 0.05, 0.075, 0.1, 0.5], 'num_iterations': [1000, 3000, 6000], 'max_depth': [100, 250, 500], 'boosting': ['gblinear', 'gbtree', 'dart']}
        },
        2241 : {
                "RFC" : {'max_depth': [4, 6, 7], 'max_leaf_nodes': [5, 10, 15, 20, 30], 'min_samples_leaf': [4, 6, 8, 10], 'min_samples_split': [6, 8, 10, 13], 'n_estimators': [5, 10, 20, 30]},
            "SVC" : {},
            "GBC" : {},
            "XGB" : {'learning_rate': [0.01, 0.05, 0.075, 0.1, 0.5], 'num_iterations': [1000, 3000, 6000], 'max_depth': [100, 250, 500], 'boosting': ['gblinear', 'gbtree', 'dart']},
            "LGBM" : {'learning_rate': [0.01, 0.05, 0.075, 0.1, 0.5], 'num_iterations': [1000, 3000, 6000], 'max_depth': [100, 250, 500], 'boosting': ['gblinear', 'gbtree', 'dart']}
        },
        369  : {
            "RFC" : {'max_depth': [4, 6, 7], 'max_leaf_nodes': [5, 10, 15, 20, 30], 'min_samples_leaf': [4, 6, 8, 10], 'min_samples_split': [18, 20, 22, 24, 28], 'n_estimators': [5, 10, 20, 30]},
            "SVC" : {'gamma': [0.01, 0.1, 0.3, 1.0, 3.0]},
            "GBC" : {},
            "XGB" : {'learning_rate': [0.01, 0.05, 0.075, 0.1, 0.5], 'num_iterations': [1000, 3000, 6000], 'max_depth': [100, 250, 500], 'boosting': ['gblinear', 'gbtree', 'dart']},
            "LGBM" : {'learning_rate': [0.01, 0.05, 0.075, 0.1, 0.5], 'num_iterations': [1000, 3000, 6000], 'max_depth': [100, 250, 500], 'boosting': ['gblinear', 'gbtree', 'dart']}
        },
        488  : {
            "RFC" : {'max_depth': [4, 6, 7], 'max_leaf_nodes': [5, 10, 15, 20, 30], 'min_samples_leaf': [4, 6, 8, 10], 'min_samples_split': [6, 8, 10, 13], 'n_estimators': [50, 100, 125]},
            "SVC" : {},
            "GBC" : {},
            "XGB" : {'learning_rate': [0.01, 0.05, 0.075, 0.1, 0.5], 'num_iterations': [1000, 3000, 6000], 'max_depth': [100, 250, 500], 'boosting': ['gblinear', 'gbtree', 'dart']},
            "LGBM" : {'learning_rate': [0.01, 0.05, 0.075, 0.1, 0.5], 'num_iterations': [1000, 3000, 6000], 'max_depth': [100, 250, 500], 'boosting': ['gblinear', 'gbtree', 'dart']}
        }
    }
}
'''