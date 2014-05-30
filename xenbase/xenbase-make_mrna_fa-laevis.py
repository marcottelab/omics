#!/usr/bin/env python
import os
import sys

filename_ncbi_list = 'NcbiMrnaXenbaseGene_laevis.txt'
filename_ncbi_fa = 'xlaevisMRNA.fasta'

## clean up version of UniGene sequence. 
## See https://github.com/marcottelab/omics/tree/master/unigene
filename_unigene_fa = '/work/xenopus/ref.XENLA/UG94/XENLA_UG94_uniq.fa'

filename_unigene_list = 'GenePageLaevisEntrezGeneUnigeneMapping.txt'
filename_nomodel_list = 'LaevisGenePages_NoModel.txt'

filename_out = 'XENLA_xb201405_mrna.fa'

names = dict()
#1008539	U35055	XB-GENE-1011632	tcf4
#1008905	L36805	XB-GENE-920327	hbox10
f_list = open(filename_ncbi_list,'r')
for line in f_list:
    tokens = line.strip().split("\t")
    tmp_gi = tokens[0]
    tmp_acc = tokens[1]
    tmp_xb = tokens[2]
    tmp_name = tokens[3]
    names[ tmp_gi ] = '%s|%s'%(tmp_name, tmp_xb)
f_list.close()

f_out = open(filename_out,'w')
f_fa = open(filename_ncbi_fa,'r')
for line in f_fa:
    if( line.startswith('>') ):
        tokens = line.strip().split()[0].split('|')
        tmp_gi = tokens[1]
        tmp_name = 'unnamed|NA'
        if( names.has_key(tmp_gi) ):
            tmp_name = names[tmp_gi]
        f_out.write('>%s|gi|%s\n'%(tmp_name,tmp_gi))
    else:
        f_out.write('%s\n'%(line.strip().upper()))
f_fa.close()

seq_list = dict()
ug_acc = ''
f_fa = open(filename_unigene_fa,'r')
for line in f_fa:
    if( line.startswith('>') ):
        tokens = line.strip().split('|')
        ug_id = tokens[0].lstrip('>')
        ug_acc = tokens[1]
        if( seq_list.has_key(ug_acc) ):
            sys.stderr.write("Duplicate:%s\n",ug_acc)
        seq_list[ug_acc] = {'id':ug_id, 'seq':[]}
    else:
        seq_list[ug_acc]['seq'].append( line.strip() )
f_fa.close()

#XB-GENE-865137	trnt1	734914	Xl.48148
#XB-GENE-6461998	foxh1.2	100337554	Xl.85732
f_list = open(filename_unigene_list,'r')
for line in f_list:
    tokens = line.strip().split("\t")
    if( len(tokens) <= 3 ):
        continue
    tmp_xb = tokens[0]
    tmp_name = tokens[1]
    tmp_ug_acc = tokens[3]
    names[ tmp_ug_acc ] = '%s|%s'%(tmp_name, tmp_xb)
    if( seq_list.has_key(tmp_ug_acc) ):
        tmp_seq = ''.join(seq_list[tmp_ug_acc]['seq'])
        tmp_id = seq_list[tmp_ug_acc]['id']
        f_out.write('>%s|%s|ug|%s\n%s\n'%(tmp_name,tmp_xb,tmp_id,tmp_seq))
f_list.close()

f_list = open(filename_nomodel_list,'r')
for line in f_list:
    tokens = line.strip().split("\t")
    tmp_xb = tokens[0]
    tmp_name = tokens[1]
    tmp_ug_acc = tokens[2]
    names[ tmp_ug_acc ] = '%s|%s'%(tmp_name, tmp_xb)
    if( seq_list.has_key(tmp_ug_acc) ):
        tmp_seq = ''.join(seq_list[tmp_ug_acc]['seq'])
        tmp_id = seq_list[tmp_ug_acc]['id']
        f_out.write('>%s|%s|ug|%s\n%s\n'%(tmp_name,tmp_xb,tmp_id,tmp_seq))
f_list.close()
f_out.close()
