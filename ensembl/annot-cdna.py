#!/usr/bin/python
import os
import sys

filename_names = sys.argv[1]
filename_prot = sys.argv[2]
filename_cdna = sys.argv[3]

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

    if( tmp_gene_name != '' ):
        names[tmp_gene_id] = tmp_gene_name.strip()
f_names.close()

coding = dict()
f_prot = open(filename_prot,'r')
for line in f_prot:
    if( line.startswith('>') ):
        tokens = line.strip().split('|')
        coding[ tokens[1] ] = tokens[0]
f_prot.close()

f_cdna = open(filename_cdna,'r')
for line in f_cdna:
    if( line.startswith('>') ):
        tokens = line.strip().lstrip('>').split('|')
        g_id = tokens[1]
        tx_id = tokens[0]
        
        tmp_name = 'NA'
        if( names.has_key(g_id) ):
            tmp_name = names[g_id]
        is_coding = 'coding'
        if( not coding.has_key(tx_id) ):
            is_coding = 'non-coding'
        print ">%s|%s|%s|%s"%(tmp_name,tx_id,g_id,is_coding)
    else:
       print line.strip()
f_cdna.close()
