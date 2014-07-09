#!/usr/bin/python
import os
import sys

filename_exon = sys.argv[1]
data_name = filename_exon.replace('.txt','')

max_exon_len = 1000
max_exon_count = 50

f_exon = open(filename_exon,'r')
headers = f_exon.readline().strip().split("\t")

gene_id_idx = headers.index('Ensembl Gene ID')
exon_id_idx = headers.index('Ensembl Exon ID')
start_pos_idx = headers.index('Exon Chr Start (bp)')
end_pos_idx = headers.index('Exon Chr End (bp)')

exon_len_list= []
gene2exon = dict()
for line in f_exon:
    tokens = line.strip().split("\t")
    tmp_gene_id = tokens[gene_id_idx]
    tmp_exon_id = tokens[exon_id_idx]
    tmp_start_pos = int(tokens[start_pos_idx])
    tmp_end_pos = int(tokens[end_pos_idx])
    tmp_exon_len = tmp_end_pos - tmp_start_pos
    if( tmp_exon_len > max_exon_len ):
        tmp_exon_len = max_exon_len
    exon_len_list.append( tmp_exon_len )

    if( not gene2exon.has_key(tmp_gene_id) ):
        gene2exon[tmp_gene_id] = dict()
    gene2exon[tmp_gene_id][tmp_start_pos] = tmp_exon_len
f_exon.close()

first_exon_len_list = []
middle_exon_len_list = []
last_exon_len_list = []
short_exon_len_list = []

gene_list = gene2exon.keys()
for tmp_gene_id in gene_list:
    tmp_pos_list = sorted(gene2exon[tmp_gene_id].keys())
    if( len(tmp_pos_list) < 3 ):
        short_exon_len_list += [gene2exon[tmp_gene_id][x] for x in tmp_pos_list]
        continue

    for tmp_i in range(0,len(tmp_pos_list)):
        if( tmp_i == 0 ):
            first_exon_len_list.append( gene2exon[tmp_gene_id][tmp_pos_list[tmp_i]] )
        elif( tmp_i == len(tmp_pos_list)-1 ):
            last_exon_len_list.append( gene2exon[tmp_gene_id][tmp_pos_list[tmp_i]] )
        else:
            middle_exon_len_list.append( gene2exon[tmp_gene_id][tmp_pos_list[tmp_i]] )

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

fig = plt.figure(figsize=(14,12))
ax1 = fig.add_subplot(2,2,1)
ax1.hist(exon_len_list,bins=range(0,max_exon_len+1,20),histtype='step',lw=2, color='black')
median_exon_len = sorted(exon_len_list)[ int(len(exon_len_list)*0.5) ]
q05_exon_len = sorted(exon_len_list)[ int(len(exon_len_list)*0.05) ]
q01_exon_len = sorted(exon_len_list)[ int(len(exon_len_list)*0.01) ]
mean_exon_len = sum(exon_len_list)*1.0/len(exon_len_list)
ax1.set_xlabel('Exon length (bp)')
ax1.set_ylabel('Frequency')
ax1.set_title('%s (N=%d)\nQ01=%d, Q05=%d, median=%d, mean=%.1f'%(data_name,len(exon_len_list),q01_exon_len, q05_exon_len, median_exon_len, mean_exon_len))
ax1.grid()

ax2 = fig.add_subplot(2,2,2)
exon_count_list = [len(gene2exon[x]) for x in gene_list]
count_single_exon = exon_count_list.count(1)
count_gtmax_exon = len([x for x in exon_count_list if x > max_exon_count])
ax2.hist(exon_count_list,bins=range(0,max_exon_count+1), histtype='step',lw=2, color='black')
ax2.set_xlabel('Number of exons per gene')
ax2.set_ylabel('Frequency')
ax2.set_title('%s (N=%d)\nsingle=%d, >%d exons=%d'%(data_name, len(exon_count_list), count_single_exon, max_exon_count, count_gtmax_exon))
ax2.grid()

ax3 = fig.add_subplot(2,2,3)
ax3.hist(first_exon_len_list, bins=range(0,max_exon_len+1,20), histtype='step', normed=1, label='First exon', lw=2, color='blue')
ax3.hist(last_exon_len_list, bins=range(0,max_exon_len+1,20), histtype='step', normed=1, label='Last exon', lw=2, color='red')
ax3.hist(middle_exon_len_list, bins=range(0,max_exon_len+1,20), histtype='step', normed=1, label='Middle exon', lw=2, color='orange')
ax3.hist(short_exon_len_list, bins=range(0,max_exon_len+1,20), histtype='step', normed=1, label='Genes with < 3 exons', lw=2, color='cyan')
ax3.legend(prop=fm.FontProperties(size=10), loc='upper center')
ax3.set_xlabel('Exon length (bp)')
ax3.set_ylabel('Normalized Frequency')
ax3.grid()

ax4 = fig.add_subplot(2,2,4)

median_len = sorted(first_exon_len_list)[ int(len(first_exon_len_list)*0.5) ]
count_gtmax = len([x for x in first_exon_len_list if x >= max_exon_len])
ax4.hist(first_exon_len_list, bins=range(0,max_exon_len+1,20), histtype='step', normed=0, color='blue', lw=2, \
        label='First exon (median=%d, >%d bp=%d)'%(median_len,max_exon_len,count_gtmax))

median_len = sorted(last_exon_len_list)[ int(len(last_exon_len_list)*0.5) ]
count_gtmax = len([x for x in last_exon_len_list if x >= max_exon_len])
ax4.hist(last_exon_len_list, bins=range(0,max_exon_len+1,20), histtype='step', normed=0, lw=2, color='red', \
        label='Last exon (median=%d, >%d bp=%d)'%(median_len,max_exon_len,count_gtmax))

median_len = sorted(middle_exon_len_list)[ int(len(middle_exon_len_list)*0.5) ]
count_gtmax = len([x for x in middle_exon_len_list if x >= max_exon_len])
ax4.hist(middle_exon_len_list, bins=range(0,max_exon_len+1,20), histtype='step', normed=0, lw=2, color='orange', \
        label='Last exon (median=%d, >%d bp=%d)'%(median_len,max_exon_len,count_gtmax))

median_len = sorted(short_exon_len_list)[ int(len(short_exon_len_list)*0.5) ]
count_gtmax = len([x for x in short_exon_len_list if x >= max_exon_len])
ax4.hist(short_exon_len_list, bins=range(0,max_exon_len+1,20), histtype='step', normed=0, lw=2, color='cyan',\
        label='Genes with <3 exons(median=%d, >%d bp=%d)'%(median_len,max_exon_len,count_gtmax))

ax4.legend(prop=fm.FontProperties(size=10), loc='upper right')
ax4.set_xlabel('Exon length (bp)')
ax4.set_ylabel('Frequency')
ax4.grid()

#plt.show()
plt.savefig('%s.exon_len_dist.png'%data_name)
