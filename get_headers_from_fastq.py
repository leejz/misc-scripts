#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 6/30/14
This script reads in an fastq and outputs the header information as a dbm file.  
   
Input fastq file
@2402:1:1101:1392:2236/2
CATAGTCTTCGGCGCCATCGTCATCCTCTACACCCTCAAGGCGAGCGGCGCGATGGAGACAATCCAGTGGGGCATGCAGCAGGTGACACCGGACTCCCGGATCCA
+
@@CFFFFFGHHHHIJJIIJIHIJIIIIJIIGEIJJIJJJJJIIIJHFFDDBD8BBD>BCBCCDDDCDCCCDBDDDDDDDDDDD<CDDDDDDDDBBCDDBD<<BDD
   
--------------------------------------------------------------------------------
usage:   get_header_from_fastq.py -i sequence.fastq 
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants

import sys
#sys.path.insert(0, '~/bin/')
from Bio import SeqIO
import shelve
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
"""Body"""
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "get_header_from_fastq.py -i sequence.fastq",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fastq", action="store", dest="inputfilename",
                        help="fastq file of input sequences")
    options = parser.parse_args()

    mandatories = ["inputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)

    inputfilename = options.inputfilename
    outputfilename = inputfilename.rpartition('.')[0] + '.headers.dbm'
   
    print("Processing fastq read file...\n"    )
 
    fastqinfile = open(inputfilename,'U')   
    header_db = shelve.open(outputfilename)
        
    for fastqcount, sequence in enumerate(SeqIO.parse(fastqinfile, "fastq")):
        header_db[str(fastqcount)] = sequence.id.strip()
    fastqinfile.close()
    header_db.close()

    print("Done!")
