#!/usr/bin/python
import os
import sys
import re

filename_fa = sys.argv[1]

seq_list = dict()
seq_h = ''
f_fa = open(filename_fa,'r')
for line in f_fa:
    if( line.startswith('>') ):
        seq_h = line.strip().lstrip('>')
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append(line.strip())
f_fa.close()

h_list = dict()
for tmp_h in seq_list.keys():
    tmp_seq = ''.join(seq_list[tmp_h])
    if( not h_list.has_key(tmp_seq) ):
        h_list[tmp_seq] = []
    h_list[tmp_seq].append(tmp_h)

filename_base = re.sub(r'.fa$','',filename_fa)
filename_base = re.sub(r'.fasta$','',filename_base)

f_NR_list = open('%s_NR.list'%filename_base,'w')
f_NR_fa = open('%s_NR.fa'%filename_base,'w')

count_dup = 0
for tmp_seq in h_list.keys():
    tmp_h_list = sorted(h_list[tmp_seq])

    if( len(h_list[tmp_seq]) == 1 ):
        f_NR_fa.write('>%s\n%s\n'%(tmp_h_list[0],tmp_seq))
    else:
        tmp_rep_id = tmp_h_list[0]
        f_NR_list.write('%s\t%s\n'%(tmp_rep_id, ';;'.join(tmp_h_list[1:])))
        sys.stderr.write('%s\t%s\n'%(tmp_rep_id, ';;'.join(tmp_h_list[1:])))
        f_NR_fa.write('>%s\n%s\n'%(tmp_rep_id,tmp_seq))
        count_dup += len(tmp_h_list)

f_NR_fa.close()
f_NR_list.close()

sys.stderr.write('Total dup: %d\n'%count_dup)
