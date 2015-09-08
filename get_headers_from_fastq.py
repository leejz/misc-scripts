#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""get_header_from_fastq.py"""
"""Jackson Lee 6/30/14"""
"""This script reads in an fastq and outputs the header information as a dbm file.  
   
   Input fastq file
   @2402:1:1101:1392:2236/2
   CATAGTCTTCGGCGCCATCGTCATCCTCTACACCCTCAAGGCGAGCGGCGCGATGGAGACAATCCAGTGGGGCATGCAGCAGGTGACACCGGACTCCCGGATCCA
   +
   @@CFFFFFGHHHHIJJIIJIHIJIIIIJIIGEIJJIJJJJJIIIJHFFDDBD8BBD>BCBCCDDDCDCCCDBDDDDDDDDDDD<CDDDDDDDDBBCDDBD<<BDD
   
   
   usage:
   get_header_from_fastq.py -i sequence.fastq 
   
"""

"""---------------------------------------------------------------------------------------"""
"""Header - Linkers, Libs, Constants"""
from string import strip
import sys
sys.path.insert(0, '~/bin/')
from Bio import SeqIO
import shelve
from optparse import OptionParser

"""function declarations"""

"""---------------------------------------------------------------------------------------"""
"""Body"""
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    get_header_from_fastq.py -i sequence.fastq",                  
    description='6/30/14 JZL get_header_from_fastq.py This script reads in an fastq and outputs the header information as a dbm file.')
    parser.add_option("-i", "--input_fastq", action="store", type="string", dest="inputfilename",
                  help="fastq file of input sequences")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)

    inputfilename = options.inputfilename
    outputfilename = inputfilename.rpartition('.')[0] + '.headers.dbm'
   
    print "Processing fastq read file...\n"    
 
    fastqinfile = open(inputfilename,'U')   
    header_db = shelve.open(outputfilename)
        
    for fastqcount, sequence in enumerate(SeqIO.parse(fastqinfile, "fastq")):
        header_db[str(fastqcount)] = sequence.id.strip()
    fastqinfile.close()
    header_db.close()

    print "Done!"
