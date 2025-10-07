#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 12/4/12
This script reads in a fasta file and a text file of numbers and filters all 
sequences in order.
   
Input fasta file format:
4098968.combined_unique.fa
   
>Sequence0000000001
GCGCCCCTACGGGGAACGTTTTACTTCCAGTTTTAAAGCAGCTTTTACCCATCCAAACTCTGCGGTAACTTTATCATAAATTGTGGTAATATCTTCTGAT   

Input filter file format:
one number per line matching the sequence order number in order. 0 being first
   
0
5
10 
22
etc.
   
Output file format:
4098968.combined_unique.filtered.fa
   
--------------------------------------------------------------------------------
usage:   filter_fasta_by_linenum.py -i input.fa -f filter.txt
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from random import shuffle

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "filter_fasta_by_linenum.py -i input.fa -f \
filter.txt",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fasta", action="store", 
                        dest="inputfilename",
                        help="fasta file of input sequences")
    parser.add_argument("-f", "--filter_text", action="store", 
                        dest="filterfilename",
                        help="filter text file (See DocString for format)")
    options = parser.parse_args()

    mandatories = ["inputfilename", "filterfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
            
    fastafilename = options.inputfilename
    filterfilename = options.filterfilename
    left, dot, right = fastafilename.rpartition('.')
    outputfilename = left +'.filtered.' + right
    
    print("Reading files...")
    with open(fastafilename,'U') as fastainfile:
        fasta_lines = [line.strip() for line in fastainfile]
    
    with open(filterfilename, 'U') as filterfile:
        linenums = [line.strip() for line in filterfile]
    
    large_fasta = []
    header = ''
    fasta = ''
    
    for iter, line in enumerate(fasta_lines):
        if line[0] == '>':
            if iter > 0:
                large_fasta.append([header,fasta])
            header = line
            fasta = ''
        else:
            fasta = fasta + line
        if iter == len(fasta_lines)-1:
            large_fasta.append([header,fasta])
            print('last line!')
    
    print("Writing Fasta file: " + outputfilename)
    with open(outputfilename, 'w') as outfile:    
        for linenum in linenums:
            outfile.write(large_fasta[int(linenum)][0]+'\n')
            outfile.write(large_fasta[int(linenum)][1]+'\n')

    print("Done!")
