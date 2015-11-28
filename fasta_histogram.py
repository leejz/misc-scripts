#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 11/8/13
Modified:  9/2015
This script reads in a fasta file and outputs a histogram file of sequence 
counts.
   
Input fasta file format:
any fasta or fastq file
   
Output file format:
bin    count
0      0
100    2
etc.

--------------------------------------------------------------------------------
usage:   fasta_histogram.py -i in.file -b bin size -o out.file
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from Bio import SeqIO
import numpy as np
import pylab as P

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = ArgumentParser(usage = "fasta_histogram.py -i in.file -b bin size -o out.file. now with FASTQ",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_file", action="store", 
                        dest="inputfilename", help="fasta input file")
    parser.add_argument("-b", "--bin_size", action="store", type=int, 
                        dest="binsize", help="bin size")
    parser.add_argument("-o", "--output_file", action="store", 
                        dest="outputfilename", help="text output file")
    options = parser.parse_args()

    mandatories = ["inputfilename", "binsize", "outputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    if options.binsize <= 0:
        print "\nError: invalid bin size\n"
        parser.print_help()
        exit(-1)
              
    inputfilename = options.inputfilename
    binsize = options.binsize
    outputfilename = options.outputfilename
  
    fasta = ['fa','fasta','fas']
    fastq = ['fq','fastq']

    if inputfilename.split('.')[-1] in fasta:
        filetype = 'fasta'
    elif inputfilename.split('.')[-1] in fastq:
        filetype = 'fastq'
    else: 
        print "Unknown file type: " + inputfilename.split('.')[-1] + ". Allowed: " + str(fastq + fasta) 
        parser.print_help()
        exit(-1)
   
    with open(inputfilename,'U') as infile:       
        fasta_lengths = [ len(rec.seq) for rec in SeqIO.parse(infile, filetype) ]      
    
    binset = range(0,max(fasta_lengths)+binsize,binsize)
    n, bins, patches = P.hist(fasta_lengths, binset, histtype='stepfilled')   
    
    fasta_lengths.sort(reverse=True)
    totalbases = sum(fasta_lengths)
    L50sum = 0
    for seq_len in fasta_lengths:
        L50sum += seq_len
        if L50sum < totalbases / 2:
            L50 = seq_len
                
    N50 = fasta_lengths.index(L50)
    
    print "N50 = ", N50, ", L50 = ", L50
    
    print "Writing file ", outputfilename
    with open(outputfilename, 'w') as outfile:
        outfile.write('bin\tlength count\n')
        for bincount, binno in zip(n,bins):
            outfile.write(str(binno)+'\t'+str(bincount)+'\n')
    
    print "Done!"
