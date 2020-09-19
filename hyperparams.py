#!/usr/bin/python3 
BASE_PATH = "data/"
SEQ_PATH = BASE_PATH + "sequence/"
STR_PATH = BASE_PATH + "structure/"
NPZ_PATH = {
    "NPInter" : "npz/NPInter.npz",
    "RPI" : {
        1807 : "npz/RPI1807.npz",
        2241 : "npz/RPI2241.npz",
        369  : "npz/RPI369.npz",
        488  : "npz/RPI488.npz"
    }
}
NPZ_PATH_STRUCT = {
    "NPInter" : "npz/STRUCT_NPInter.npz",
    "RPI" : {
        1807 : "npz/STRUCT_RPI1807.npz",
        2241 : "npz/STRUCT_RPI2241.npz",
        369  : "npz/STRUCT_RPI369.npz",
        488  : "npz/STRUCT_RPI488.npz"
    }
}
Z_NPZ_PATH = {
    "NPInter" : "npz/Z_NPInter.npz",
    "RPI" : {
        1807 : "npz/Z_RPI1807.npz",
        2241 : "npz/Z_RPI2241.npz",
        369  : "npz/Z_RPI369.npz",
        488  : "npz/Z_RPI488.npz"
    }
}
LOG_NPZ_PATH = {
    "NPInter" : "npz/LOG_NPInter.npz",
    "RPI" : {
        1807 : "npz/LOG_RPI1807.npz",
        2241 : "npz/LOG_RPI2241.npz",
        369  : "npz/LOG_RPI369.npz",
        488  : "npz/LOG_RPI488.npz"
    }
}
LOG_Z_NPZ_PATH = {
    "NPInter" : "npz/LOG_Z_NPInter.npz",
    "RPI" : {
        1807 : "npz/LOG_Z_RPI1807.npz",
        2241 : "npz/LOG_Z_RPI2241.npz",
        369  : "npz/LOG_Z_RPI369.npz",
        488  : "npz/LOG_Z_RPI488.npz"
    }
}
LOG_M_NPZ_PATH = {
    "NPInter" : "npz/LOG_M_NPInter.npz",
    "RPI" : {
        1807 : "npz/LOG_M_RPI1807.npz",
        2241 : "npz/LOG_M_RPI2241.npz",
        369  : "npz/LOG_M_RPI369.npz",
        488  : "npz/LOG_M_RPI488.npz"
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


PARAM_GRID = {
    "NPInter" : {
        "RFC" : {'max_depth': [7, 8, 9], 'max_leaf_nodes': [5, 10, 15, 20, 30], 'min_samples_leaf': [15, 18, 21, 24, 30], 'min_samples_split': [6, 8, 10, 13], 'n_estimators': [50, 100, 125]},
        "SVC" : {},
        "GBC" : {},
        "XGB" : {'boosting': ['gblinear'], 'learning_rate': [0.5], 'max_depth': [100], 'num_iterations': [1000]},
        "LGBM" : {'boosting': ['gblinear'], 'learning_rate': [0.5], 'max_depth': [100], 'num_iterations': [1000]}
    },
    "RPI" : {
        1807 : {
            "RFC" : {'max_depth': [7], 'max_leaf_nodes': [30], 'min_samples_leaf': [18], 'min_samples_split': [6], 'n_estimators': [100]},
            "SVC" : {},
            "GBC" : {},
            "XGB" : {'learning_rate': [0.1], 'num_iterations': [1000], 'max_depth': [100], 'boosting': ['gblinear']}
        },
        2241 : {
            "RFC" : {'max_depth': [7], 'max_leaf_nodes': [30], 'min_samples_leaf': [6], 'min_samples_split': [13], 'n_estimators': [5]},
            "SVC" : {},
            "GBC" : {},
            "XGB" : {'learning_rate': [0.075], 'num_iterations': [1000], 'max_depth': [100], 'boosting': ['gblinear']}
        },
        369  : {
            "RFC" : {'max_depth': [6], 'max_leaf_nodes': [10], 'min_samples_leaf': [8], 'min_samples_split': [20], 'n_estimators': [30]},
            "SVC" : {},
            "GBC" : {},
            "XGB" : {'learning_rate': [0.1], 'num_iterations': [1000], 'max_depth': [100], 'boosting': ['gblinear']},
            "LGBM" : {'boosting': ['dart'], 'learning_rate': [0.075], 'max_depth': [100], 'num_iterations': [1000]}
        },
        488  : {
            "RFC" : {'max_depth': [6], 'max_leaf_nodes': [10], 'min_samples_leaf': [7], 'min_samples_split': [13], 'n_estimators': [125]},
            "SVC" : {},
            "GBC" : {},
            "XGB" : {'learning_rate': [0.075], 'num_iterations': [1000], 'max_depth': [100], 'boosting': ['gblinear']},
            "LGBM" : {'boosting': ['dart'], 'learning_rate': [0.01], 'max_depth': [100], 'num_iterations': [1000]}
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
            "SVC" : {},
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