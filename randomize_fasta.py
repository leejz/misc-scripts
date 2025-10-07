#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 12/4/12

This script reads in a fasta file and randomizes the lines
   
Input fasta file format:
4098968.combined_unique.fa
   
>Sequence0000000001
GCGCCCCTACGGGGAACGTTTTACTTCCAGTTTTAAAGCAGCTTTTACCCATCCAAACTCTGCGGTAACTTTATCATAAATTGTGGTAATATCTTCTGAT   

Output file format:
same
   
--------------------------------------------------------------------------------
usage:   randomize_fasta.py -i input.fa -o output_fasta
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
    parser = ArgumentParser(usage = "randomize_fasta.py -i input.fa -o output.fa",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fasta", action="store", 
                        dest="inputfilename",
                        help="fasta file of input sequences")
    parser.add_argument("-o", "--output_fasta", 
                        action="store", dest="outputfilename",
                        help="output fasta file name")
    options = parser.parse_args()

    mandatories = ["inputfilename", "outputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
            
    fastafilename = options.inputfilename
    outputfilename = options.outputfilename
    
    print("Reading Fasta file...")
    with open(fastafilename,'U') as fastainfile:
        fasta_lines = [line.strip() for line in fastainfile]
    
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
    
    print("Writing randomized Fasta file: " + outputfilename)

    shuffle(large_fasta)    
    with open(outputfilename, 'w') as outfile:    
        for fastaline in large_fasta:
            outfile.write(fastaline[0]+'\n')
            outfile.write(fastaline[1]+'\n')

    print("Done!")
