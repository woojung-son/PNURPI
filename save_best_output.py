
import json
from collections import OrderedDict
from Logger import *
import glob
import os.path

def save_best_output(npz_path, best_score, best_params, best_model) :
    
    datasets = ['NPInter', 'RPI369', 'RPI488', 'RPI1807', 'RPI2241']

    for dataset in datasets :
        if dataset in npz_path :
            targetDataset = dataset

    current_score_dict = {
        "dataset" : npz_path,
        "best_score" : best_score,
        "best_params" : best_params,
        "best_model" : best_model.replace('\t', ' ').replace(' ', '')
    }
    
    result_dict = {
            "NPInter" : {
                "dataset" : '',
                "best_score" : 0,
                "best_params" : {},
                "best_model" : {}
            },
            "RPI1807" : {
                "dataset" : '',
                "best_score" : 0,
                "best_params" : {},
                "best_model" : {}
            },
            "RPI2241" : {
                "dataset" : '',
                "best_score" : 0,
                "best_params" : {},
                "best_model" : {}
            },
            "RPI369"  : {
                "dataset" : '',
                "best_score" : 0,
                "best_params" : {},
                "best_model" : {}
            },
            "RPI488"  : {
                "dataset" : '',
                "best_score" : 0,
                "best_params" : {},
                "best_model" : {}
            }
        }
    
    file = './best_output.json'

    if not os.path.exists(file) : 

        fp = open('best_output.json', 'w', encoding='UTF-8')
        
        fp.write(json.JSONEncoder().encode(result_dict))
        fp.close()
    
    fp = open('best_output.json', 'r+', encoding='UTF-8')
    data_json = json.load(fp)
    best_score_so_far = data_json[targetDataset]["best_score"]
    logger.debug('[save_best_output]best_score_so_far : {}'.format(best_score_so_far))
    
    if best_score > best_score_so_far :
        data_json[targetDataset] = current_score_dict
        logger.debug('[save_best_output]Best Score of dataset {0} updated with score {1}'.format(targetDataset, best_score))
        
    fp.close()
        
    with open('best_output.json', 'w', encoding='utf-8') as fp:
        json.dump(data_json, fp, indent="\t")
