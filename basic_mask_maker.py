#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:  Jackson Lee 5/19/12
Read in a mask fasta file and export a filter mask that is mothur/qiime 
compatible.  The syntax of this script emulates the original
   
input file:
fasta file [0-9A-L] quality scores.  From Arb help:
'0123456789ABC...'
The higher the number the more conserved
+2 half mutations
eg. '7' half number of mutations than '5'
   
>pos_var_Bacteria_102        669 bp          rna
E-G--IH--JD-----E---------------------------------------------------------I-D--H-CE--D-C-GH-I-
output file:
#1533 columns
0000000000001110111100000110010110101010110010110101010010100101010100101010100101001010101000

--------------------------------------------------------------------------------   
usage:    basic_mask_maker.py -i filter.fasta -a A -o outfile.filter

NOTE: This is a basic mask maker script.  No error checking is done!
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from sys import argv
from re import split
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "basic_mask_maker.py -i filter.fasta -a A \
-o outfile.filter",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fasta", action="store", 
                        dest="inputfilename",
                        help="fasta file of input sequences")
    parser.add_argument("-o", "--outfile_filter", action="store", 
                        dest="outfilename",
                        help="output filter file")    
    parser.add_argument("-a", "--cutoff", action="store", dest="cutoff",
                        help="cutoff score for filter")
    options = parser.parse_args()

    mandatories = ["inputfilename", "outfilename", "cutoff"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
    
    # read in command line args and parse file
    inputfilename = options.inputfilename
    outfilename=options.outfilename
    cutoff = options.cutoff
        
    with open(inputfilename, 'U') as infile:
        cutoffscores='0123456789ABCDEFGHIJKL'
        cutoffval=cutoffscores.index(cutoff)
        header=infile.next().strip()
        sequence=infile.next().strip()
        print(len(sequence),"bp sequence read")
        output_sequence=''
        for letter in sequence:
            if letter == '-':
                outputletter='0'
            elif cutoffval <= cutoffscores.index(letter):
                outputletter='1'
            elif cutoffval >  cutoffscores.index(letter): 
                outputletter='0'
            else:
                print('no match for letter', letter, 'at position',len(output_sequence))
            output_sequence+=outputletter

    with open(outfilename, 'w') as outfile:
        outheader=split('\W+',header)
        outfile.write('#'+outheader[2]+' '+outheader[3]+'\n')
        outfile.write(output_sequence)
        print(len(output_sequence), "bp filter written to", outfilename)

    print("Done!")
