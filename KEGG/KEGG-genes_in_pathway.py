#!/usr/bin/env python
import os
import sys

for filename in os.listdir('.'):
    if( not filename.startswith('path:') ):
        continue
    sys.stderr.write('Read %s ... '%filename)

    path_id = ''
    path_name = ''
    gene_list = []

    prev_tag = ''
    f = open(filename,'r')
    for line in f:
        tmp_tag = line[:11].strip()
        if( tmp_tag == 'ENTRY' ):
            path_id = line.strip().split()[1]
        if( tmp_tag == 'NAME' ):
            path_name = line[11:].split(' - ')[0].strip()
        if( tmp_tag == 'GENE' ):
            gene_list.append( line[11:].strip().split()[0] )
        elif( tmp_tag == '' and prev_tag == 'GENE' ):
            gene_list.append( line[11:].strip().split()[0] )

        if( tmp_tag != '' ):
            prev_tag = tmp_tag
    f.close()       
    sys.stderr.write('%s(%d) %s\n'%(path_id, len(gene_list), path_name))
    
    print "%s\t%s\t%s"%(path_id, path_name, ";;".join(sorted(gene_list)))
