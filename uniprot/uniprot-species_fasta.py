#!/usr/bin/python
import os
import sys
import gzip

usage_mesg = 'Usage: %s <species_code>'%sys.argv[0]

species_code = sys.argv[1]

if( not os.access('reldate.txt',os.R_OK) ):
    sys.stderr.write('reldate.txt does not exist. Please run wget.sh first.\n')
    sys.exit(1)

f_rel_date = open('reldate.txt','r')
rel_date = f_rel_date.readline().strip().split()[3].replace('_','')
sys.stderr.write('Release date: %s\n'%rel_date)
f_rel_date.close()

filename_out_base = '%s_uniprot%s'%(species_code,rel_date)

if( not os.access('speclist',os.R_OK) ):
    sys.stderr.write('speclist does not exist. Please run wget.sh first.\n')
    sys.exit(1)

confirm_species_code = 0
f_spec_list = open('speclist','r')
for line in f_spec_list:
    tokens = line.strip().split()
    if( len(tokens) == 0 ):
        continue
    if( tokens[0] == species_code ):
        sys.stderr.write('%s\n'%line.strip())
        confirm_species_code = 1
f_spec_list.close()

if( confirm_species_code == 0 ):
    sys.stderr.write('%s is not available in speclist.\n'%species_code)
    sys.exit(1)

def read_fasta(filename, sp_code):
    rv = dict()
    is_selected = 0
    f = gzip.open(filename,'rb')
    for line in f:
        if( line.startswith('>') ):
            tmp_id = line.strip().split()[0].lstrip('>')
            tmp_sp_code = tmp_id.split('_')[-1]
            if( tmp_sp_code == sp_code ):
                is_selected = 1
                rv[tmp_id] = []
            else:
                is_selected = 0
        elif( is_selected > 0 ):
            rv[tmp_id].append( line.strip() )
    f.close()
    return rv

sys.stderr.write('Read sprot...')
sprot_seq = read_fasta('uniprot_sprot.fasta.gz', species_code)
sys.stderr.write('Done\nRead trembl...')
trembl_seq = read_fasta('uniprot_trembl.fasta.gz', species_code)
sys.stderr.write('Done\n')

seq2h = dict()
for tmp_h in sprot_seq.keys():
    tmp_seq = ''.join(sprot_seq[tmp_h])
    if( not seq2h.has_key(tmp_seq) ):
        seq2h[tmp_seq] = []
    seq2h[tmp_seq].append(tmp_h)

for tmp_h in trembl_seq.keys():
    tmp_seq = ''.join(trembl_seq[tmp_h])
    if( not seq2h.has_key(tmp_seq) ):
        seq2h[tmp_seq] = []
    seq2h[tmp_seq].append(tmp_h)

count_single = 0
count_multi = 0

f_out_fa = open('%s.fa'%filename_out_base,'w')
f_out_log = open('%s.NR_log'%filename_out_base,'w')
for tmp_seq in seq2h.keys():
    tmp_h_list = sorted(list(set(seq2h[tmp_seq])))
    if( len(tmp_h_list) == 1 ):
        tmp_rep_h = tmp_h_list[0]
        f_out_fa.write('>%s\n%s\n'%(tmp_rep_h,tmp_seq))
        count_single += 1
    else:
        tmp_rep_h = tmp_h_list[0]
        f_out_fa.write('>%s\n%s\n'%(tmp_rep_h,tmp_seq))
        f_out_log.write('%s\t%s\n'%(tmp_rep_h,';;'.join(tmp_h_list[1:])))
        count_multi += len(tmp_rep_h)
f_out_fa.close()
f_out_log.close()
