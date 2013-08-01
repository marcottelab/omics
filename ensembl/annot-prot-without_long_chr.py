#!/usr/bin/python
import os
import sys

filename_names = sys.argv[1]
filename_prot = sys.argv[2]

names = dict()

f_names = open(filename_names,'r')
headers = f_names.readline().strip().split("\t")
idx_gene_id = headers.index('Ensembl Gene ID')
idx_chr_name = headers.index('Chromosome Name')
idx_gene_name = headers.index('Associated Gene Name')

for line in f_names:
    tokens = line.split("\t")
    tmp_gene_id = tokens[idx_gene_id]
    tmp_gene_name = tokens[idx_gene_name].strip().replace(':','_').replace(' ','')
    tmp_chr_name = tokens[idx_chr_name]

    if( len(tmp_chr_name) > 2 ):
        continue

    if( tmp_gene_name == '' ):
        names[tmp_gene_id] = 'NA'
    else:
        names[tmp_gene_id] = tmp_gene_name.strip()
f_names.close()

is_print = 0
f_prot = open(filename_prot,'r')
for line in f_prot:
    if( line.startswith('>') ):
        tokens = line.strip().lstrip('>').split('|')
        gene_id = tokens[-1]
        if( not names.has_key(gene_id) ):
            is_print = 0
            continue
        
        is_print = 1
        print ">%s|%s"%(names[gene_id],'|'.join(tokens))
    
    elif( is_print > 0 ):
        print line.strip()
f_prot.close()
