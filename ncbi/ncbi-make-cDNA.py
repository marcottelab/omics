#!/usr/bin/python
import os
import sys

gb_id = sys.argv[1]

def check_file(filename):
    if( not os.access(filename,os.R_OK) ):
        print "%s is not available."%filename
        sys.exit(1)

filename_fna = "%s.fna"%gb_id
filename_ptt = "%s.ptt"%gb_id
check_file(filename_fna)
check_file(filename_ptt)

annot = dict()
is_start = 0
f_ptt = open(filename_ptt,'r')
for line in f_ptt:
    if( line.startswith('Location') ):
        is_start = 1
        continue
    if( is_start == 0 ):
        continue

    tokens = line.strip().split("\t")
    gene_name = 'unnamed'
    if( tokens[4] != '' ):
        gene_name = tokens[4]
    annot[tokens[3]] = '%s|%s|%s|%s'%(gene_name,tokens[3],tokens[0],tokens[1])
f_ptt.close()

seq_list = []
f_fa = open(filename_fna,'r')
for line in f_fa:
    if( not line.startswith('>') ):
        seq_list.append( line.strip() )
f_fa.close()

cmp_map = {'A':'T','T':'A','G':'C','C':'G','N':'N'}
def revcomp(tmp_seq):
    rv = []
    for tmp_n in tmp_seq[::-1]:
        rv.append( cmp_map[tmp_n] )
    return ''.join(rv)

seq = ''.join(seq_list)
for gi in annot.keys():
    pos_tokens = annot[gi].split('|')[2].split('..')
    tmp_seq = seq[int(pos_tokens[0])-1:int(pos_tokens[1])]
    if( annot[gi].endswith('-') ):
        tmp_seq = revcomp(tmp_seq)
    print ">%s\n%s"%(annot[gi],tmp_seq)
