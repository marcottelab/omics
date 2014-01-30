#!/bin/bash
## PATHWAY_LIST is from http://rest.kegg.jp/get/<species_code>

PATHWAY_LIST=$1
awk '{print "wget http://rest.kegg.jp/get/"$1}' $PATHWAY_LIST 
