#!/usr/bin/env python
import os
import sys

filename_fna = sys.argv[1]
filename_gff = sys.argv[2]

filename_base = filename_gff.split('.')[0]

acc_id = ''
seq_list = dict()
f_fa = open(filename_fna,'r')
for line in f_fa:
    if( line.startswith('>') ):
        acc_id = line.strip().split('|')[3]
        seq_list[acc_id] = ''
    else:
        seq_list[acc_id] += line.strip().upper()
f_fa.close()

rc = {'A':'T','T':'A','G':'C','C':'G','N':'N'}
def revcomp(tmp_seq):
    return ''.join([rc[x] for x in tmp_seq[::-1]])

def parse_cdna(tmp_seq, tmp_start, tmp_end, tmp_strand):
    rv = tmp_seq[tmp_start-1:tmp_end]
    if( tmp_strand == '-' ):
        return revcomp(rv)
    return rv

## http://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG11
AAs  =   'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
Starts = '---M---------------M------------MMMM---------------M------------'
Base1  = 'TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG'
Base2  = 'TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG'
Base3  = 'TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG'
trans_tbl = dict()

for i in range(0,len(AAs)):
    trans_tbl['%s%s%s'%(Base1[i],Base2[i],Base3[i])] = AAs[i]

def translate(tmp_nseq):
    rv = []
    for i in range(0,len(tmp_nseq)-2,3):
        tmp_codon = tmp_nseq[i:i+3]
        if( not trans_tbl.has_key(tmp_codon) ):
            rv.append('*')
        else:
            rv.append( trans_tbl[tmp_codon] )
    return ''.join(rv)


f_cdna = open('%s_cdna.fa'%filename_base,'w')
f_pep = open('%s_pep.fa'%filename_base,'w')
gene2name = dict()
f_gff = open(filename_gff,'r')
for line in f_gff:
    if( line.startswith('#') ):
        continue
    tokens = line.strip().split("\t")
    tmp_type = tokens[2]
    tmp_start = int(tokens[3])
    tmp_end = int(tokens[4])
    tmp_strand = tokens[6]

    tmp_name = ''
    tmp_id = ''
    tmp_parent = ''
    for tmp in tokens[8].split(';'):
        if( tmp.startswith('Name=') ):
            tmp_name = tmp.split('=')[1]
        if( tmp.startswith('ID=') ):
            tmp_id = tmp.split('=')[1]
        if( tmp.startswith('Parent=') ):
            tmp_parent= tmp.split('=')[1]

    if( tokens[2] == 'gene' ):
        tmp_cdna = parse_cdna(seq_list[tokens[0]],tmp_start, tmp_end, tmp_strand)
        gene2name[tmp_id] = tmp_name
        sys.stderr.write('Write %s @ cdna (%d)\n'%(tmp_name, len(tmp_cdna)))
        f_cdna.write('>%s\n%s\n'%(tmp_name,tmp_cdna))

    if( tokens[2] == 'CDS' ):
        tmp_cdna = parse_cdna(seq_list[tokens[0]],tmp_start, tmp_end, tmp_strand)
        tmp_pep = translate(tmp_cdna)
        tmp_name = gene2name[tmp_parent]
        sys.stderr.write('Write %s @ pep (%d)\n'%(tmp_name, len(tmp_pep)))
        f_pep.write('>%s\n%s\n'%(tmp_name,tmp_pep))
f_cdna.close()
f_pep.close()
