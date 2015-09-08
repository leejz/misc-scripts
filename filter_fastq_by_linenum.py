#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""filter_fastq_by_linenum.py"""
"""Jackson Lee 7/1/14"""
"""This script reads in a fastq file and a text file of numbers and filters all sequences in order
   
   Input fasta file format:
   Input fastq file
   @2402:1:1101:1392:2236/2
   CATAGTCTTCGGCGCCATCGTCATCCTCTACACCCTCAAGGCGAGCGGCGCGATGGAGACAATCCAGTGGGGCATGCAGCAGGTGACACCGGACTCCCGGATCCA
   +
   @@CFFFFFGHHHHIJJIIJIHIJIIIIJIIGEIJJIJJJJJIIIJHFFDDBD8BBD>BCBCCDDDCDCCCDBDDDDDDDDDDD<CDDDDDDDDBBCDDBD<<BDD
   

   Input filter file format:
   one number per line matching the sequence order number in order. 0 being first
   
   0
   5
   10 
   22
   etc.
   
   Output file format:
   sequence.filtered.fastq
   
   usage:
   filter_fastq_by_linenum.py -i input.fastq -f filter.txt
"""

"""---------------------------------------------------------------------------------------"""
"""Header - Linkers, Libs, Constants"""
from string import strip
from optparse import OptionParser
import sys
sys.path.insert(0, '~/bin/')
from Bio import SeqIO

"""---------------------------------------------------------------------------------------"""

"""function declarations"""

def process_and_generate(input_iterator, filterfile, filterflag):
    """Reusable function that processes a record, then generates each record.

    input_iterator is an iterator that returns one record at a time
    process_function is a function that takes one record and does some
      processing on it
    """    
    for count, rec in input_iterator:
        global linenum_next
        if filterflag:
            if count+1 == linenum_next:
                linenum_next = int(filterfile.next().strip())
            else:
                #print count+1
                yield rec
        else:
            if count+1 == linenum_next:
                linenum_next = int(filterfile.next().strip())
                #print count+1
                yield rec
"""---------------------------------------------------------------------------------------"""

"""Body"""
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    filter_fastq_by_linenum.py -i input.fastq -f filter.txt",                  
    description='7/1/14 JZL filter_fastq_by_linenum.py.  reads in a fastq file and text file and filters sequences by line number')
    parser.add_option("-i", "--input_fasta", action="store", type="string", dest="inputfilename",
                  help="fastq file of input sequences")
    parser.add_option("-f", "--filter_text", action="store", type="string", dest="filterfilename",
                  help="filter text file (See DocString for format)")
    parser.add_option("-r", "--reverse_filter_flag", action="store_true", dest="reverseflag", default=False,
                  help="set to enable exclusion filtering")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "filterfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
            
    inputfilename = options.inputfilename
    filterfilename = options.filterfilename
    left, __, right = inputfilename.rpartition('.')
    outputfilename = left +'.filtered.' + right
    
    filterfile = open(filterfilename, 'U') 
    linenum_next = int(filterfile.next().strip())
    inputfile = open(inputfilename, 'U')
    outfile = open(outputfilename, 'w')   
                    
    print "Opening and parsing..."
    if options.reverseflag:        
        print "Exclusion filtering enabled.  Saving sequences not in " + filterfilename 
        outputfilename = left +'.exclusion.filtered.' + right
    outfile = open(outputfilename, 'w')
    parse_iterator = SeqIO.parse(inputfile, "fastq")
    record_generator = enumerate(parse_iterator) 
    SeqIO.write(process_and_generate(record_generator, filterfile, options.reverseflag), outfile, "fastq")     

    #SeqIO.write([fastq_record for fastqcount, fastq_record in enumerate(SeqIO.parse(inputfile, "fastq")) if fastqcount+1 in linenums], outfile, "fastq")     
    #for fastqcount, fastq_record in enumerate(SeqIO.parse(inputfile, "fastq")):
    #    if fastqcount+1 in linenums:
            #print "seq " + str(fastqcount)
    #        linenums.remove(fastqcount)
    #        SeqIO.write(fastq_record, outfile, "fastq") 
    outfile.close()
    filterfile.close()
	
    print "Done!"
