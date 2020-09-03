
from sklearn.svm import SVC
from sklearn.model_selection import validation_curve
from sklearn.model_selection import GridSearchCV



def SVM_Classifying(X, y, KFOLD_TIME) : 
    SVMC = SVC(probability=True)
    param_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
    #svc_param_grid = [{'gamma': param_range, 'C':param_range, 'kernal': ['rbf']},
    #                 {'gamma': param_range, 'C':param_range, 'kernal': ['linear']}]
    param_grid = {
        'gamma': param_range,
        'random_state' : [2]
    }
    print('test1')
    #print(sorted(estimator.get_params().keys()))
    #['C', 'break_ties', 'cache_size', 'class_weight', 'coef0', 'decision_function_shape', 'degree', 'gamma', 'kernel', 'max_iter', 'probability', 'random_state', 'shrinking', 'tol', 'verbose']


    gsSVMC = GridSearchCV(SVMC, param_grid = param_grid, cv=KFOLD_TIME,
                         scoring="accuracy", n_jobs=1, verbose=1)
    print('test2')
    print(sorted(SVMC.get_params().keys()))

    gsSVMC.fit(X, y)

    SVMC_best = gsSVMC.best_estimator_
    print(gsSVMC.best_score_)
    # Best score
    return gsSVMC.best_score_
