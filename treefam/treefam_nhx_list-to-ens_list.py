#!/usr/bin/python
import os
import sys

f_list = open('treefam_clean_nhx.list','r')
f_out = open('treefam_ens.list','w')
for line in f_list:
    tmp_path = line.strip()
    tf_id = tmp_path.split('/')[2]
    sys.stderr.write('%s\n'%(tf_id))
    ensg_list = []
    f_nhx = open(tmp_path,'r')
    for line in f_nhx:
        if( line.find('ENS') > 0 ):
            ensg_id = line.strip().split(':G=')[-1].split(':')[0].rstrip(',]')
            if( ensg_id.startswith('ENS') ):
                ensg_list.append(ensg_id)
    f_nhx.close()
    ensg_list = list(set(ensg_list))
    if( len(ensg_list) == 0 ):
        continue
    f_out.write("%s\t%s\n"%(tf_id,','.join(ensg_list)))
f_list.close()
f_out.close()
