#!/usr/bin/env python
import os
import sys
import gzip

filename_seq = sys.argv[1]

seq_list = dict()
ug_id = ''

f_fa = open(filename_seq,'r')
if( filename_seq.endswith('.gz') ):
    f_fa = gzip.open(filename_seq,'rb')

for line in f_fa:
    if( line.startswith('>') ):
        tokens = line.strip().split()
        ug_id = tokens[0].split('|')[2].replace('#','_')
        ug_acc = [x.replace('/ug=','') for x in tokens if x.startswith('/ug=')][0]
        gi = [x.replace('/gi=','') for x in tokens if x.startswith('/gi=')][0]
        seq_list[ug_id] = {'acc':ug_acc, 'gi':gi, 'seq':[]}
    else:
        seq_list[ug_id]['seq'].append( line.strip().upper() )
f_fa.close()

for ug_id in sorted(seq_list.keys()):
    tmp = seq_list[ug_id]
    print ">%s|%s|%s\n%s"%(ug_id, tmp['acc'], tmp['gi'], ''.join(tmp['seq']))
