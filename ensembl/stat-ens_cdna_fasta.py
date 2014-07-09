#!/usr/bin/python
import os
import sys

gene_list = []
seq_list = dict()
seq_len = dict()
seq_h = ''
f = open(sys.argv[1],'r')
for line in f:
    if( line.startswith('>') ):
        tokens = line.strip().split()
        #gene_id = tokens[-1].replace('gene:','')
        #seq_h = '%s|%s'%(tokens[0],gene_id)
        seq_h = line.strip().lstrip('>')
        gene_id = seq_h.split('|')[-1]

        seq_list[seq_h] = []
        seq_len[seq_h] = 0
        gene_list.append(gene_id)
    else:
        seq_list[seq_h].append( line.strip() )
        seq_len[seq_h] += len(line.strip())
f.close()

gene_list = list(set(gene_list))
seq_len_list = sorted(seq_len.values())
median_len = seq_len_list[ int(len(seq_len_list)*0.5) ]
bottom10_len = seq_len_list[ int(len(seq_len_list)*0.1) ]

print "Total gene:%d, Total Tx:%d, >500bp:%d, >1kbp:%d, median:%d, bottom 10pct: %d"%(len(gene_list),len(seq_len_list), len([x for x in seq_len_list if x > 500]),len([x for x in seq_len_list if x > 1000]), median_len, bottom10_len)
#for seq_h in sorted(seq_list.keys()):
#    print "%s\n%s"%(seq_h,''.join(seq_list[seq_h]))
