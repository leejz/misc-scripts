#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""Jackson Lee 5/19/12"""
"""Read in a mask fasta file and export a filter mask that is mothur/qiime compatible.  The
   syntax of this script emulates the original
   
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
   
   usage:
   python basic_mask_maker.py <filter.fasta> <AN> <outfile.filter>
   where filter.fasta is the input file
   AN is a single letter mutation variation cutoff score 0-9A-L to make mask
   outfile.filter is the output filename
   """
"""---------------------------------------------------------------------------------------"""
"""Header - Linkers, Libs, Constants"""
from string import strip
from sys import argv
from re import split
from optparse import OptionParser

"""function declarations"""

"""---------------------------------------------------------------------------------------"""
"""Body"""
print "This is a basic mask maker script.  No error checking is done!"
print "Running..."


if __name__ == '__main__':
    parser = OptionParser(usage = "usage: basic_mask_maker.py -i filter.fasta -a A -o outfile.filter",                  
    description='5/19/12 JZL basic_mask_maker.py.  Read in FASTA filter file and make a hard filter (see docstring for format)')
    parser.add_option("-i", "--input_fasta", action="store", type="string", dest="inputfilename",
                  help="fasta file of input sequences")
    parser.add_option("-o", "--outfile_filter", action="store", type="string", dest="outfilename",
                  help="output filter file")    
    parser.add_option("-a", "--cutoff", action="store", type="string", dest="cutoff",
                  help="cutoff score for filter")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "outfilename", "cutoff"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    
    # read in command line args and parse file
    inputfilename = options.inputfilename
    outfilename=options.outfilename
    
    infile = open(inputfilename, 'U')
    outfile = open(outfilename, 'w')  

    cutoffscores='0123456789ABCDEFGHIJKL'
    
    cutoff = options.cutoff
    cutoffval=cutoffscores.index(cutoff)
    header=infile.next().strip()
    sequence=infile.next().strip()
    print len(sequence),"bp sequence read"
    output_sequence=''
    for letter in sequence:
        if letter == '-':
             outputletter='0'
        elif cutoffval <= cutoffscores.index(letter):
             outputletter='1'
        elif cutoffval >  cutoffscores.index(letter): 
             outputletter='0'
        else:
             print 'no match for letter', letter, 'at position',len(output_sequence)
        output_sequence+=outputletter
    infile.close()

    outheader=split('\W+',header)
    outfile.write('#'+outheader[2]+' '+outheader[3]+'\n')
    outfile.write(output_sequence)
    print len(output_sequence), "bp filter written to", outfilename
    outfile.close()

    print "Done!"