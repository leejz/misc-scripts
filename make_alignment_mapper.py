#!/usr/bin/python
"""This script reads in the ecoli reference alignment in a particular format and generates
   a mapping file which assigns a sequential count of each base pair to the current alignment
   position.  Specifically, this script is used to build a mapping file to convert silva alignments
   into ecoli position counts for comparison of data with an alignment reference to the whole
   16S structure.
   
   usage:
   make_alignment_mapper.py 
   
   alignment infile format:
   a single fasta sequence with header removed formatted into the mapping alignment
   
   outfile format (infile.mapping):
   1	1
   2	1
   3	1
   4	2
   5	3
   etc
"""
   
from string import strip

"""------------------------------------------------------------------------------------------"""
# Load files
print "Running..."

alignmentfilename= 'ecoli_SAI.fixed.fasta' 
outfilename= alignmentfilename+'.mapping'

#open file
alignmentfile=open(alignmentfilename,'U')
outfile=open(outfilename,'w')

line=alignmentfile.readline().strip()
columncount=0
ecoli=0
for character in line:
	columncount+=1
	if character in ['A','T','G','C','U']:
		ecoli+=1
	outline=str(columncount)+'\t'+str(ecoli)+'\n'
	outfile.write(outline)

alignmentfile.close()
outfile.close()
print "Done!"