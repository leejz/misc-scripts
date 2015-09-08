#!/usr/bin/env python

"""---------------------------------------------------------------------------------------
Jackson Lee 8/4/15
Quick script to convert fasta/qual to fastq

http://seqanswers.com/forums/showthread.php?t=16925

from Bio import SeqIO
from Bio.SeqIO.QualityIO import PairedFastaQualIterator
handle = open("temp.fastq", "w") #w=write
records = PairedFastaQualIterator(open("example.fasta"), open("example.qual"))
count = SeqIO.write(records, handle, "fastq")
handle.close()
print "Converted %i records" % count

---------------------------------------------------------------------------------------"""

#Header - Linkers, Libs, Constants

from Bio import SeqIO
from Bio.SeqIO.QualityIO import PairedFastaQualIterator
from optparse import OptionParser


#---------------------------------------------------------------------------------------

#function declarations


             

#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    fasta_to_fastq.py -i input.fasta -q qual.txt -o output.fastq",
    description="Jackson Lee 8/4/15 Quick script to convert fasta/qual to fastq")
    parser.add_option("-i", "--input_fasta", action="store", type="string", dest="fastaname",
                  help="fasta file")
    parser.add_option("-q", "--qual_file", action="store", type="string", dest="qualname",
                  help="paired 454 qual file")
    parser.add_option("-o", "--output_fastq", action="store", type="string", dest="outputfastqname",
                  help="output fastq file")                  
    (options, args) = parser.parse_args()

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