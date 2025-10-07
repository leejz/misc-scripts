#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:  Jackson Lee 12/4/12
This script reads in a fasta file and a text file of headers and filters all 
sequences in the file by exact match.  The script produces a not in file output 
as well.
   
Input fasta file format:
4098968.combined_unique.fa
   
>Sequence0000000001
GCGCCCCTACGGGGAACGTTTTACTTCCAGTTTTAAAGCAGCTTTTACCCATCCAAACTCTGCGGTAACTTTATCATAAATTGTGGTAATATCTTCTGAT   

Input filter file format:
>Sequence0000000001
   
0
5
10 
22
etc.
   
Output file format:
4098968.combined_unique.filtered.fa

--------------------------------------------------------------------------------
usage:   filter_fasta_by_header.py -i input.fa -f filter.txt -n flipflag
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "filter_fasta_by_header.py -i input.fa -f \
filter.txt -n flipflag",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fasta", action="store", 
                        dest="inputfilename",
                        help="fasta file of input sequences")
    parser.add_argument("-f", "--filter_text", action="store", 
                        dest="filterfilename", help="filter header file")
    parser.add_argument("-n", "--flipflag", action="store_true", dest="flipflag",
                        help="use to include rather than exclude filter sequences")
    options = parser.parse_args()

    mandatories = ["inputfilename", "filterfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
            
    flipflag = options.flipflag
    if flipflag:
        print("flipflag found, this script will keep only fasta sequences NOT in the filter list" )
    else:
        print("this script will keep only fasta sequences in the filter list" )
    fastafilename = options.inputfilename
    filterfilename = options.filterfilename
    left, dot, right = fastafilename.rpartition('.')
    outputfilename = left +'.filtered.' + filterfilename.partition('.')[0] + dot + right
    badoutputsfilename = left + '.notinlist.txt'
    
    filterfile = open(filterfilename, 'U')
    lineheaders = []
    for line in filterfile:
        if line[0] == '>':
            lineheaders.append(line.strip()[1:])
        else:
            lineheaders.append(line.strip())
    lineheaders = set(lineheaders)
    filterfile.close()
    
    fastainfile = open(fastafilename,'U')
    linecount = 0
    for line in fastainfile:
        linecount += 1
    fastainfile.close()
    
    
    print("Writing Fasta file: " + outputfilename)
    fastainfile = open(fastafilename,'U')
    outfile = open(outputfilename, 'w')
    badoutputsfile = open(badoutputsfilename, 'w')
        
    header = ''
    fasta = ''
    matchflag = False 
        
    for i, line in enumerate(fastainfile):
        if line[0] == '>':
            if matchflag == True:
                matchflag = False
                outfile.write(fasta + '\n')
            if not flipflag:
                if line.strip()[1:] in lineheaders:
                    outfile.write(line)
                    matchflag = True
                    fasta = ''
                else:
                    badoutputsfile.write(line)
                    matchflag = False
            else:
                if line.strip()[1:] not in lineheaders:
                    outfile.write(line)
                    matchflag = True
                    fasta = ''
                else:
                    badoutputsfile.write(line)
                    matchflag = False
        else:
            fasta = fasta + line.strip()
            # catch case of match on last line of file
            if i == linecount-1 and matchflag == True:
                outfile.write(fasta + '\n')

    fastainfile.close()
    outfile.close()
    badoutputsfile.close()

    print("Done!")
