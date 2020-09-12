
import json
from collections import OrderedDict
from Logger import *


'''{
    "json_string": "string_example",
    "json_number": 100,
    "json_array": [1, 2, 3, 4, 5],
    "json_object": { "name":"John", "age":30},
    "json_bool": true
}'''
def save_best_output(npz_path, best_score, best_params, best_model) :
    
    datasets = ['NPInter', 'RPI369', 'RPI488', 'RPI1807', 'RPI2241']

    #npz/LOG_NPInter.npz

    for dataset in datasets :
        if dataset in npz_path :
            targetDataset = dataset
    
    current_score_dict = {
        "dataset" : npz_path,
        "best_score" : best_score,
        "best_params" : best_params,
        "best_model" : str(best_model)
    }

    # with를 이용해 파일을 연다.
    # json 파일은 같은 폴더에 있다고 가정!
    fp = open('best_output.json', 'w+', encoding='UTF-8')
    data_str = fp.readlines()
    
    if len(data_str) <= 0 :
        #print('len : {}'.format(len(data_str)))
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
            },
        }
        #print(json.JSONEncoder().encode(result_dict))
        fp.write(json.JSONEncoder().encode(result_dict))
    fp.close()
    
    fp = open('best_output.json', 'r+', encoding='UTF-8')
    data_json = json.load(fp)
    print('targetDataset : {}'.format(targetDataset))
    best_score_so_far = data_json[targetDataset]["best_score"]
    
    if best_score > best_score_so_far :
        data_json[targetDataset] = current_score_dict
        logger.debug('Best Score of dataset {0} updated with score {1}'.format(targetDataset, best_score))
        
    fp.close()
        
    with open('best_output.json', 'w', encoding='utf-8') as fp:
        json.dump(data_json, fp, indent="\t")
        
    #with open('best_output.json', 'r') as f:
    #    json_data = json.load(f)
    #    print(json.dumps(json_data, indent="\t") )

