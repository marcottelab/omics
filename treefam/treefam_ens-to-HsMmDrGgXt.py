#!/usr/bin/python
import os
import sys

f_list = open('treefam_ens.list','r')

for line in f_list:
    tokens = line.strip().split("\t")
    TF_id = tokens[0]
    ensg_list = []
    for tmp_id in tokens[1].split(','):
        if( tmp_id.startswith('ENSG0') ):
            ensg_list.append(tmp_id)
        if( tmp_id.startswith('ENSMUS') ):
            ensg_list.append(tmp_id)
        if( tmp_id.startswith('ENSDAR') ):
            ensg_list.append(tmp_id)
        if( tmp_id.startswith('ENSGAL') ):
            ensg_list.append(tmp_id)
        if( tmp_id.startswith('ENSXET') ):
            ensg_list.append(tmp_id)
    
    if( len(ensg_list) <= 1 ):
        continue
    print "%s\t%s"%(TF_id,','.join(sorted(ensg_list)))
f_list.close()
