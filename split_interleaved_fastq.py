#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 9/18/14
This script reads in an fastq file and splits the interleaved file into a 1 and 
2 mate pair of fastq files.
   
Input fastq file
@HISEQ06:204:C06F3ACXX:5:1101:1475:2407 1:N:0
CAAANGCGCCCTCATCGAGCGGACGCTGACGCATGTCGACCTCGACGCGCAGCCCTTGAAAACGATCCTCGGCTGGGTCGAACTGGGCGAGAGAAAACGTCCCGACCTCGAATCCGCCTACTACGATATCCTGCTGACGCCGTTCGTG
+
CCCF#2ADHHHHHJJJJJJJJJJJJJJJJJJJJJJHJIHGFFFFDDDDDDDDDDDDDDDDDDDDDDCDDDDDDDDDDCDDDDDDDCABD@D>BDDCDCDBDDD>BDD>CD@CC@CBDB@DDC:@?<8(0:AA:@CCC?BDDD@9<BBD
@HISEQ06:204:C06F3ACXX:5:1101:1475:2407 2:N:0
GGGCGAGGGGTCCTTCGCCACGAACGGCGTCAGCAGGATATCGTAGTAGGCGGATTCGAGGTCGGGACGTTTTCTCTCGCCCAGTTCGACCCAGCCGAGGATCGTTTTCAAGGGCTGCGCGTCGAGGTCGACATGCGTCAGCGTCCGC
+
BCCFFFFFHHDHHGHIJJJJJJJJJJJJJIHHHFFFFDEEEEDDDDDEDDDDDDDDDDEDD7CBDD@BD;BDDDDDDDDDDDDDDDDDDDDDDDDDD>BD@CCDCDDDDDDCDBBBDDDDDDDDBBD0?<9>3&4:>BB@<@B<@>9>

--------------------------------------------------------------------------------
usage:   split_interleaved_fastq.py -i sequence.fastq    
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from Bio import SeqIO
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

def writeline_fastq(record, file):
    """write a single fastq record to a file"""    
    file.write(record.id + '\n')
    file.write(record.seq + '\n')
    file.write('+\n')
    file.write(record.letter_annotations + '\n')            

#-------------------------------------------------------------------------------
"""Body"""
print "Running..."

if __name__ == '__main__':
    parser = ArgumentParser(usage = "split_interleaved_fastq.py -i sequence.fastq",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fastq", action="store", 
                        dest="inputfilename",
                        help="fastq file of input sequences")
    parser.add_argument("-f", "--mate_format", action="store", 
                        dest="mate_format", default = ' ',
                        help="fastq file illumina mate format (' ' default, '/' for older illimuna reads")
    options = parser.parse_args()

    mandatories = ["inputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
   
    if options.mate_format not in ('/', ' '):
        print "\nError: Invalid mate read delimiter"
        parser.print_help()
        exit(-1)
    else:
        mate_format = options.mate_format

    inputfilename = options.inputfilename
    infile = open(inputfilename,'U')      
    left, _, right = inputfilename.rpartition('.')
    outputfilename1 = left + '.1.' + right
    outputfilename2 = left + '.2.' + right
    
    parse_iterator = SeqIO.parse(infile, "fastq")
        
    print "Processing fastq read file...\n"        
    
    with open(inputfilename, 'U') as inputfile, open(outputfilename1, 'w') as out1, open(outputfilename2, 'w') as out2:
        for record in parse_iterator:
            next_rec = parse_iterator.next()
            nex_name, nex_mate = next_rec.description.split(mate_format)
            cur_name, cur_mate = record.description.split(mate_format)
            
            if nex_mate == '2' and cur_mate == '1' and nex_name == cur_name:
                out1.write(record.format("fastq"))
                out2.write(next_rec.format("fastq"))
    
    print "Done!"
