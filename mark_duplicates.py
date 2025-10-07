#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 1/16/15

This script reads in a fasta file and outputs a list file of all duplicates.  
This script is not memory optimized and may struggle with large 
(full MiSeq/HiSeq) runs.

Input file format:
fasta or fastq
   
output format:
scaffold-111	scaffold-112	scaffold-113	etc...
scaffold-21	scaffold-22	etc...
...

--------------------------------------------------------------------------------
usage:   mark_duplicates.py -i fa.file -o out.txt
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import csv
import numpy as np	
from Bio import SeqIO

#-------------------------------------------------------------------------------
#function declarations

    
#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "mark_duplicates.py -i fa.file -o out.txt",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fasta", action="store", 
                        dest="inputfilename",
                        help="input fasta file") 
    parser.add_argument("-o", "--output_filename", action="store", 
                        dest="outputfilename",
                        help="output tab delimited data file")
    options = parser.parse_args()

    mandatories = ["inputfilename", "outputfilename"]
    
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)

    inputfilename = options.inputfilename
    outputfilename = options.outputfilename
        
    with open(inputfilename, 'U') as infile:
        parse_iterator = SeqIO.parse(infile, "fasta")
        seq_dict = {}
        for record in parse_iterator:
            sequence = str(record.seq)
            if sequence in seq_dict:
                seq_dict[sequence].append(record.description)
            else:
                seq_dict[sequence] = [record.description]
                
    with open(outputfilename, 'w') as outfile:
        writer = csv.writer(outfile, dialect='excel-tab')
        for seq_names in seq_dict.values():
            if len(seq_names) > 1:
                writer.writerow(seq_names)
                
    print("Done!")
