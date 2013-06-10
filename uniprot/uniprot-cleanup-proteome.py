#!/usr/bin/python
import os
import sys

filename_fa = sys.argv[1]

seq_list = dict()
seq_h = ''
f_fa = open(filename_fa,'r')
for line in f_fa:
    if( line.startswith('>') ):
        tokens = line.strip().split()
        tmp_id = tokens[0].lstrip('>')
        tmp_name = 'UNNAMED'
        for tmp in tokens:
            if( tmp.startswith('GN=') ):
                tmp_name = tmp.replace('GN=','')
                break
        seq_h = '%s|%s'%(tmp_id,tmp_name) 
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append(line.strip())
f_fa.close()

for tmp_h in seq_list.keys():
    tmp_seq = ''.join(seq_list[tmp_h])
    print ">%s\n%s"%(tmp_h,tmp_seq)
