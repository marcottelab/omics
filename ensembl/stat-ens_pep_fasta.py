#!/usr/bin/python
import os
import sys
import gzip

filename = sys.argv[1]

seq_list = dict()
seq_len = dict()
seq_h = ''

f = open(filename,'r')
if( filename.endswith('.gz') ):
    f = gzip.open(filename,'rb')
for line in f:
    if( line.startswith('>') ):
        tokens = line.strip().split()
        seq_h = '%s|%s|%s'%(tokens[-2].replace('gene:',''),tokens[-1].replace('transcript:',''),tokens[0].lstrip('>'))
        seq_list[seq_h] = []
        seq_len[seq_h] = 0
    else:
        seq_list[seq_h].append( line.strip() )
        seq_len[seq_h] += len(line.strip())
f.close()

seq_len_list = sorted(seq_len.values())
median_len = seq_len_list[ int(len(seq_len_list)*0.5) ]

sys.stderr.write("Total:%d, >500bp:%d, >1kbp:%d, median:%d\n"%(len(seq_len_list), len([x for x in seq_len_list if x > 500]),len([x for x in seq_len_list if x > 1000]), median_len))
for seq_h in sorted(seq_list.keys()):
    print ">%s\n%s"%(seq_h,''.join(seq_list[seq_h]))
