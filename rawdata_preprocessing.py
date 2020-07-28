#!/usr/bin/python3 
from hyperparams import *
isPrint = False
###############################################################################
# fasta methods
###############################################################################
from Bio import SeqIO

def read_fasta_file(fpath):
    fasta_sequences = SeqIO.parse(open(fpath),'fasta')
    seq_dict = {}
    for i, fasta in enumerate(fasta_sequences):
        name, sequence = fasta.id, str(fasta.seq)
        if isPrint : print(name, sequence)
        seq_dict[name] = sequence        
    return seq_dict

def read_RPI_fasta(size):
    rna_seq_path = SEQ_PATH["RPI"][size]["RNA"]
    rna_seqs = read_fasta_file(rna_seq_path)
    protein_seq_path = SEQ_PATH["RPI"][size]["Protein"]
    protein_seqs = read_fasta_file(protein_seq_path)
    return rna_seqs, protein_seqs

def read_NPInter_fasta():
    rna_seq_path = SEQ_PATH["NPInter"]["RNA"]
    rna_seqs = read_fasta_file(rna_seq_path)
    protein_seq_path = SEQ_PATH["NPInter"]["Protein"]
    protein_seqs = read_fasta_file(protein_seq_path)
    return rna_seqs, protein_seqs

###############################################################################
# Pair methods
###############################################################################

def read_pair_file(fpath):
    f = open(fpath, "r")
    flines = f.readlines()
    pairs = []
    for line in flines:
        line = line.replace("\n","")
        p1, p2, label = line.split("\t")
        
        if isPrint : 
            print("P1: {} / P2: {} / Label: {}".format(p1,p2,label))
        
        pairs.append((p1,p2,label))
    return pairs

def read_RPI_pairs(size):
    pair_path = PAIRS_PATH["RPI"][size] #/data/RPI369_pairs.txt 에서 데이터 읽어옴 (1drz-A, 1drz-B, 1) 형식 
    pairs = read_pair_file(pair_path) # (1drz-A, 1drz-B, 1) (맨 마지막껀 레이블, 첫번째 두번째껀 잘 모르겠음) 이 원소로 들어있는 배열 생성
    return pairs

def read_NPInter_pairs():
    pair_path = PAIRS_PATH["NPInter"]
    pairs = read_pair_file(pair_path)
    return pairs

###############################################################################
# Pair-Seq methods
###############################################################################

def read_RPI_pairSeq(size):
    X, Y = [], []
    pairs = read_RPI_pairs(size) 
    # /data/RPI369_pairs.txt 의 파일을 읽어 [(1drz-A, 1drz-B, 1), (1drz-A, 1drz-B, 1), ...] 형식의 배열 반환 
    rseq, pseq = read_RPI_fasta(size) 
    # /data/sequence/RPI369_protein_seq.fa 의 key, value값이 dic 형태로 저장되어서 pseq에 반환됨. rseq는 RNA파일
    # pairs에는 protein_id값이, pseq에는 id와 value쌍의 dic이 저장.
    for protein_id, rna_id, label in pairs:
        X.append([pseq[protein_id], rseq[rna_id]])
        Y.append(int(label))
    
    return X, Y 
# X : 2차원 배열 [[protein value1, rna value1], [protein value1, rna value1], ... ]
# Y : 1차원 배열. label의 배열 [1, 1, 1, ... , 0, 0, 0]

def read_NPInter_pairSeq():
    X, Y = [], []
    pairs = read_NPInter_pairs()
    rseq, pseq = read_NPInter_fasta()
    for protein_id, rna_id, label in pairs:
        X.append([pseq[protein_id], rseq[rna_id]])
        Y.append(int(label))
    
    return X, Y

if __name__ == "__main__":
    # Example
    read_RPI_pairSeq(369)
    read_NPInter_pairSeq()