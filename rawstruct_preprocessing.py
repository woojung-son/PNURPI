
#from hyperparams import *
isPrint = False
import string
import Bio

DATASET_DICT = {369 : 'RPI369', 488 : 'RPI488', 1807 : 'RPI1807', 2241 : 'RPI2241', 10412 : 'NPInter'}
BASE_PATH = "data/"
SEQ_PATH = BASE_PATH + "sequence/"
STR_PATH = BASE_PATH + "structure/"

def read_data_pair(path):
    # _pair.txt (RNA sequence, Protein sequence, label 을 묶어서 pair을 표시해놓은 파일) 을 열어서 결합하는거끼리, 안하는거끼리 2차원 배열 2개를
    # 만드는 함수.
    pos_pairs = []
    neg_pairs = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            p, r, label = line.split('\t')
            if label == '1':
                pos_pairs.append((p, r))
            elif label == '0':
                neg_pairs.append((p, r))
    return pos_pairs, neg_pairs

def read_data_seq(path):
    print('path of what we\'ve preprocessing : {}'.format(path))
    # .fa 파일을 읽어서 (번호 : seqneuce) 이렇게 딕셔너리를 만들어주는 함수.
    seq_dict = {}
    with open(path, 'r') as f:
        name = ''
        for line in f:
            line = line.strip()
            if line[0] == '>':
                name = line[1:]
                seq_dict[name] = ''
            else:
                if line.startswith('XXX'):
                    seq_dict.pop(name)
                else:
                    seq_dict[name] = line
    return seq_dict
    
def read_RPI_pairStruct(size=10412) :
    pro_seqs = read_data_seq(SEQ_PATH + DATASET_DICT[size] + '_protein_seq.fa')
    rna_seqs = read_data_seq(SEQ_PATH + DATASET_DICT[size] + '_rna_seq.fa')
    pro_structs = read_data_seq(STR_PATH + DATASET_DICT[size] + '_protein_struct.fa')
    rna_structs = read_data_seq(STR_PATH + DATASET_DICT[size] + '_rna_struct.fa')
    pos_pairs, neg_pairs = read_data_pair(BASE_PATH + DATASET_DICT[size] + '_pairs.txt')

    return pos_pairs, neg_pairs, pro_seqs, rna_seqs, pro_structs, rna_structs
