#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""Jackson Lee 12/4/12"""
"""This script reads in a fasta file and a text file of numbers and filters all sequences in order
   
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
   
   usage:
   filter_fasta_by_linenum.py -i input.fa -f filter.txt
"""

"""---------------------------------------------------------------------------------------"""
"""Header - Linkers, Libs, Constants"""
from string import strip
from optparse import OptionParser
from random import shuffle

"""function declarations"""

"""---------------------------------------------------------------------------------------"""
"""Body"""
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    filter_fasta_by_linenum.py -i input.fa -f filter.txt",                  
    description='2/7/13 JZL filter_fasta_by_linenum.py.  reads in a fasta file and text file and filters sequences by line number')
    parser.add_option("-i", "--input_fasta", action="store", type="string", dest="inputfilename",
                  help="fasta file of input sequences")
    parser.add_option("-f", "--filter_text", action="store", type="string", dest="filterfilename",
                  help="filter text file (See DocString for format)")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "filterfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
            
    fastafilename = options.inputfilename
    filterfilename = options.filterfilename
    left, dot, right = fastafilename.rpartition('.')
    outputfilename = left +'.filtered.' + right
    
    print "Reading files..."
    fastainfile = open(fastafilename,'U')
    fasta_lines = [line.strip() for line in fastainfile]
    fastainfile.close()
    
    filterfile = open(filterfilename, 'U')
    linenums = [line.strip() for line in filterfile]
    filterfile.close()
    
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
            print 'last line!'
    
    print "Writing Fasta file: " + outputfilename
    outfile = open(outputfilename, 'w')
    
    for linenum in linenums:
        outfile.write(large_fasta[int(linenum)][0]+'\n')
        outfile.write(large_fasta[int(linenum)][1]+'\n')

    outfile.close()

    print "Done!"
