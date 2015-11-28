#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:  Jackson Lee 8/4/15

Quick script to convert fasta/qual to fastq

from:
http://seqanswers.com/forums/showthread.php?t=16925

from Bio import SeqIO
from Bio.SeqIO.QualityIO import PairedFastaQualIterator
handle = open("temp.fastq", "w") #w=write
records = PairedFastaQualIterator(open("example.fasta"), open("example.qual"))
count = SeqIO.write(records, handle, "fastq")
handle.close()
print "Converted %i records" % count

--------------------------------------------------------------------------------
usage:   fasta_to_fastq.py -i input.fasta -q qual.txt -o output.fastq
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants

from Bio import SeqIO
from Bio.SeqIO.QualityIO import PairedFastaQualIterator
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations
    
#-------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = ArgumentParser(usage = "fasta_to_fastq.py -i input.fasta -q qual.txt\
 -o output.fastq",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fasta", action="store", 
                        dest="fastaname", help="fasta file")
    parser.add_argument("-q", "--qual_file", action="store", dest="qualname",
                        help="paired 454 qual file")
    parser.add_argument("-o", "--output_fastq", action="store", 
                        dest="outputfastqname", help="output fastq file")                  
    options = parser.parse_args()

    mandatories = ["fastaname", "qualname", "outputfastqname"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    fastaname = options.fastaname            
    qualname = options.qualname        
    outputfastqname = options.outputfastqname

print "Parsing: " + outputfastqname

with open(outputfastqname, 'w') as handle, open(fastaname, 'U') as fastafile, open(qualname, 'U') as qualfile:
    records = PairedFastaQualIterator(fastafile, qualfile)
    count = SeqIO.write(records, handle, "fastq")
    print "Converted %i records" % count
    
print "Done!"