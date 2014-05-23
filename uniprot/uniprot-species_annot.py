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
        sys.stderr.write('Species in "speclist": %s\n'%line.strip())
        confirm_species_code = 1
f_spec_list.close()

if( confirm_species_code == 0 ):
    sys.stderr.write('%s is not available in speclist.\n'%species_code)
    sys.exit(1)

def read_head(filename, sp_code):
    rv = dict()
    is_selected = 0
    f = gzip.open(filename,'rb')
    for line in f:
        if( line.startswith('>') ):
            tokens = line.strip().split()
            tmp_id = tokens[0].lstrip('>')
            tmp_sp_code = tmp_id.split('_')[-1]
            if( tmp_sp_code == sp_code ):
                rv[tmp_id] = ' '.join(tokens[1:])
    f.close()
    return rv

sys.stderr.write('Read sprot...')
sprot_h = read_head('uniprot_sprot.fasta.gz', species_code)
sys.stderr.write('Done\nRead trembl...')
trembl_h = read_head('uniprot_trembl.fasta.gz', species_code)
sys.stderr.write('Done\n')

f_out = open('%s_annot.txt'%filename_out_base,'w')
for tmp_h in sorted(sprot_h.keys()):
    f_out.write("%s\t%s\n"%(tmp_h,sprot_h[tmp_h]))
for tmp_h in sorted(trembl_h.keys()):
    f_out.write("%s\t%s\n"%(tmp_h,trembl_h[tmp_h]))
f_out.close()
