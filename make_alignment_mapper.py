#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 2012
This script reads in the ecoli reference alignment in a particular format and 
generates a mapping file which assigns a sequential count of each base pair to 
the current alignment position.  Specifically, this script is used to build a 
mapping file to convert silva alignments into ecoli position counts for 
comparison of data with an alignment reference to the whole 16S structure.
   
alignment infile format:
a single fasta sequence with header removed formatted into the mapping alignment
   
   outfile format (infile.mapping):
   1	1
   2	1
   3	1
   4	2
   5	3
   etc


--------------------------------------------------------------------------------
usage: make_alignment_mapper.py -a alignment.fasta
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip

#-------------------------------------------------------------------------------
#Body
print("Running...")

#Header - Linkers, Libs, Constants
from string import strip
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import csv
#import pandas as pd

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "make_aligment_mapper.py -a alignment.fasta",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-a", "--fasta_file", action="store", dest="alignmentfilename",
                  help="SILVA output fasta FAI")
    options = parser.parse_args()

    mandatories = ["alignmentfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
            
alignmentfilename= options.alignmentfilename
outfilename= alignmentfilename+'.mapping'

#open file
with open(alignmentfilename,'U') as alignmentfile, open(outfilename,'w') as outfile:
    line=alignmentfile.readline().strip()
    columncount=0
    ecoli=0
    for character in line:
        columncount+=1
        if character in ['A','T','G','C','U']:
	        ecoli+=1
        outline=str(columncount)+'\t'+str(ecoli)+'\n'
        outfile.write(outline)

print("Done!")
