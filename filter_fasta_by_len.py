#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:  Jackson Lee 7/8/14
This script reads in a fasta or fastq and filters for sequences greater or less 
than a threshold length
   
Input fastq file
@2402:1:1101:1392:2236/2
GATAGTCTTCGGCGCCATCGTCATCCTCTACACCCTCAAGGCGAGCGGCGCGATGGAGACAATCCAGTGGGGCATGCAGCAGGTGACACCGGACTCCCGGATCCA
+
@@CFFFFFGHHHHIJJIIJIHIJIIIIJIIGEIJJIJJJJJIIIJHFFDDBD8BBD>BCBCCDDDCDCCCDBDDDDDDDDDDD<CDDDDDDDDBBCDDBD<<BDD
   
--------------------------------------------------------------------------------
usage:   filter_fasta_by_len.py -i sequence.fasta -g filter_greater_than -l filter_less_than 
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from Bio import SeqIO
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

def process_and_generate(input_iterator, threshold, greaterflag):
    """Reusable function that processes a record, then generates each record.

    input_iterator is an iterator that returns one record at a time
    process_function is a function that takes one record and does some
      processing on it
    """    
    for rec in input_iterator:
        if greaterflag:
            if len(rec.seq) <= threshold:
                yield rec
        else:
            if len(rec.seq) >= threshold:
                yield rec

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "filter_fasta_by_len.py -i sequence.fasta -g filter_greater_than -l filter_less_than",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fastq", action="store", 
                        dest="inputfilename",
                        help="fastq file of input sequences")
    parser.add_argument("-g", "--filter_greater_than", action="store", type=int, 
                        dest="greaterthan",
                        help="filter out sequences greater than or equal to \
this size")
    parser.add_argument("-l", "--filter_less_than", action="store", type=int, 
                        dest="lessthan",
                        help="filter out sequences less than or equal this size")
    options = parser.parse_args()

    mandatories = ["inputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)

    inputfilename = options.inputfilename
    left, __, right = inputfilename.rpartition('.')
    fasta =['fa','fasta','faa','fas', 'fna']
    fastq =['fq','fastq']
    if right in fasta:
        ext = "fasta"
    elif right in fastq:
        ext = "fastq"

    print("Processing read file: " + inputfilename        )
    
    with open(inputfilename,'U') as infile:    
        parse_iterator = SeqIO.parse(infile, ext)
        if options.greaterthan == None and options.lessthan == None:
            print("\nError: Missing Comparison Value\n")
            parser.print_help()
            exit(-1)
        elif options.greaterthan == None and options.lessthan != None:
            lessthan = options.lessthan
            print("and filtering out sequences less than ", lessthan)
            outputfilename = left + '.filtered.lessthan.' + str(lessthan) + "." + right
            with open(outputfilename, 'w') as outfile:
                record_generator = process_and_generate(parse_iterator, lessthan, False)
                SeqIO.write(record_generator, outfile, ext)     
        elif options.greaterthan != None and options.lessthan == None:
            greaterthan = options.greaterthan
            print("and filtering out sequences greater than ", greaterthan)
            outputfilename = left + '.filtered.greaterthan.' + str(greaterthan) + "." + right
            with open(outputfilename, 'w') as outfile:
                record_generator = process_and_generate(parse_iterator, greaterthan, True)
                SeqIO.write(record_generator, outfile, ext)     
        elif options.greaterthan != None and options.lessthan != None: 
            greaterthan = options.greaterthan
            lessthan = options.lessthan
            print("and filtering out sequences less than ", lessthan, " and greater than ", greaterthan)
            outputfilename = left + '.filtered.greaterthan.' + str(greaterthan) + ".filtered.lessthan." + str(lessthan) + '.' + right
            with open(outputfilename, 'w') as outfile:
                pre_record_generator = process_and_generate(parse_iterator, greaterthan, True)
                record_generator = process_and_generate(pre_record_generator, lessthan, False)
                SeqIO.write(record_generator, outfile, ext)     


    print("Done!")
