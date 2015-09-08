#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
generate_contig_len.py
Jackson Lee 11/26/14
This script reads in an fasta and outputs a tab delimited length file   
   
   usage:
   generate_contig_len.py -i sequence.fasta -o contig.lengths.txt
   


---------------------------------------------------------------------------------------"""
#Header - Linkers, Libs, Constants
from string import strip
from Bio import SeqIO
from optparse import OptionParser

#---------------------------------------------------------------------------------------

#function declarations

def process_and_generate(input_iterator, threshold, greaterflag):
    """Reusable function that processes a record, then generates each record.

    input_iterator is an iterator that returns one record at a time
    process_function is a function that takes one record and does some
      processing on it
    """    
    for rec in input_iterator:
        if greaterflag:
            if len(rec.seq) >= threshold:
                yield rec
        else:
            if len(rec.seq) < threshold:
                yield rec

#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    generate_contig_len.py -i sequence.fasta -o contig.lengths.txt",                  
    description=' 11/26/14 This script reads in an fasta and outputs a tab delimited length file')
    parser.add_option("-i", "--input_fastq", action="store", type="string", dest="inputfilename",
                  help="fastq file of input sequences")
    parser.add_option("-o", "--output_file", action="store", type="string", dest="outputfilename",
                  help="tab-delimited length text file")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "outputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)

    inputfilename = options.inputfilename
    outputfilename = options.outputfilename  
    
    print "Processing fasta file...\n"            
    with open(inputfilename,'U') as infile, open(outputfilename, 'w') as outfile:
        parse_iterator = SeqIO.parse(infile, "fasta")
        for seqrec in parse_iterator:
            outfile.write(str(seqrec.id) + '\t' + str(len(seqrec.seq)) + '\n')                

    print "Done!"
