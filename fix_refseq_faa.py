#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 8/27/12
Read in lines of a fasta file and remove protein sequence new lines
   
input file:
fasta file 
    
>gi|41178954|ref|NP_957541.1| putative mobilization protein A [Moraxella catarrhalis]
MASFERTLMAGLNQDRYNILWVEHTDKDRLELNFLIPKVDLGTGKAMNPYFDKTDRGLVDVWKQVINYDYGLHDPDDPKN
RQTLVTVKDLPKSKQEFKQALTAVLEQKILADEIKDHADIIKELENMGLEIARTTPTAISIKDPDGGRNIRLKGEIYEQT

output file:
same, but without newlines
   
--------------------------------------------------------------------------------
usage:    python fix_refseq_faa.py -i input.fasta -o outfilename.fasta
"""
#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from re import split
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "python fix_refseq_faa.py -i input.fasta -o \
outfilename.fasta",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fasta", action="store", 
                        dest="inputfilename",
                        help="fasta file of input sequences")
    parser.add_argument("-o", "--outfile_filter", action="store", 
                        dest="outfilename",
                        help="output fasta file name")    
    options = parser.parse_args()

    mandatories = ["inputfilename", "outfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
    
    # read in command line args and parse file
    inputfilename = options.inputfilename
    outfilename=options.outfilename
    
    with open(inputfilename, 'U') as infile, open(outfilename, 'w') as outfile:   
        for linenum, line in enumerate(infile):
            if line[0] == ">":
                if linenum != 0:
                    outline = "\n" + line
                else:
                    outline = line[:]
                outfile.write(outline)
            elif line.strip().isupper():
                outfile.write(line.strip())
    print(str(linenum)+" lines written")

    print("Done!")
