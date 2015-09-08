#!/usr/bin/python
"""This script reads a list of positions and remaps them to the new position based on a mapping
   alignment file.
   
   usage:
   remap_alignment.py 
   
   mapping infile format:
   a single fasta sequence with header removed formatted into the mapping alignment
   1	1
   2	1
   3	1
   4	2
   5	3
   etc
   
   infile format:
   1
   1
   3
   5
   etc
   
   outfile format (infile.mapping):
   1
   1
   1
   3
   etc
"""
   
from string import strip

"""------------------------------------------------------------------------------------------"""
# Load files
print "Running..."

mappingfilename= 'ecoli_SAI.fixed.fasta.mapping' 
infilename='chimera_window.txt'
outfilename= mappingfilename+'.remapped'

#open file
mappingfile=open(mappingfilename,'U')
infile=open(infilename,'U')
outfile=open(outfilename,'w')

mappingdict={}
for line in mappingfile:
	mappingdictkey, mappingdictval=line.strip().split('\t')
	mappingdict[mappingdictkey]=mappingdictval

for line in infile:
	lookupval=line.strip()
	remapval=mappingdict[lookupval]
	outline=str(remapval)+'\n'
	outfile.write(outline)

mappingfile.close()
infile.close()
outfile.close()
print "Done!"