#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 8/27/12
Read in a text file of gi names and then pull those fasta sequences out of a 
fasta file. This script will also output a not in list file.
   
input file:
gi list:
a text file with one gi number on each line
    
fasta file     
>gi|41178954|ref|NP_957541.1| putative mobilization protein A [Moraxella catarrhalis]
MASFERTLMAGLNQDRYNILWVEHTDKDRLELNFLIPKVDLGTGKAMNPYFDKTDRGLVDVWKQVINYDYGLHDPDDPKN
RQTLVTVKDLPKSKQEFKQALTAVLEQKILADEIKDHADIIKELENMGLEIARTTPTAISIKDPDGGRNIRLKGEIYEQT

output file:
same, but with only the selected files

--------------------------------------------------------------------------------   
usage:    python extract_fasta_with_gi.py -i input.fasta -g input.list.txt -o output.fasta
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
print "Running..."


if __name__ == '__main__':
    parser = ArgumentParser(usage = "python extract_fasta_with_gi.py -i \
input.fasta -g input.list.txt -o output.fasta",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fasta", action="store", 
                        dest="inputfilename",
                        help="fasta file of input sequences")
    parser.add_argument("-o", "--outfile_filter", action="store", 
                        dest="outfilename",
                        help="output fasta file name")    
    parser.add_argument("-g", "--gi_list", action="store", dest="gi_list",
                        help="text file of list")   
    options = parser.parse_args()

    mandatories = ["inputfilename", "outfilename", "gi_list"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    
    # read in command line args and parse file
    inputfilename = options.inputfilename
    outfilename=options.outfilename
    gilistname=options.gi_list
    
    infile = open(inputfilename, 'U')
    outfile = open(outfilename, 'w')  
    gifile = open(gilistname, 'U')
    
    gilist = []
    for line in gifile:
        gilist.append(line.strip())
    gifile.close()
    
    pullnextflag=False
    for line in infile:
        if line[0] == ">":
            giname = line.strip().split('|')[1]
            if giname in gilist:
                outfile.write(line)
                gilist.pop(gilist.index(giname))
                pullnextflag = True
        elif pullnextflag == True:
            outfile.write(line)
            pullnextflag = False

    print "Files written.  The following gi's not found:\n"
    print [ginames+"\n" for ginames in gilist]
    infile.close()
    outfile.close()

    print "Done!"