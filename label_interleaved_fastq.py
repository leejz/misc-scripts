#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
label_interleaved_fastq.py
Jackson Lee 9/18/14
This script reads in an fastq file and fixes duplicate sequence names so a mate pair file can be generated
   
   Input fastq file
@HISEQ06:204:C06F3ACXX:5:1101:1475:2407 1:N:0
CAAANGCGCCCTCATCGAGCGGACGCTGACGCATGTCGACCTCGACGCGCAGCCCTTGAAAACGATCCTCGGCTGGGTCGAACTGGGCGAGAGAAAACGTCCCGACCTCGAATCCGCCTACTACGATATCCTGCTGACGCCGTTCGTG
+
CCCF#2ADHHHHHJJJJJJJJJJJJJJJJJJJJJJHJIHGFFFFDDDDDDDDDDDDDDDDDDDDDDCDDDDDDDDDDCDDDDDDDCABD@D>BDDCDCDBDDD>BDD>CD@CC@CBDB@DDC:@?<8(0:AA:@CCC?BDDD@9<BBD
@HISEQ06:204:C06F3ACXX:5:1101:1475:2407 1:N:0
GGGCGAGGGGTCCTTCGCCACGAACGGCGTCAGCAGGATATCGTAGTAGGCGGATTCGAGGTCGGGACGTTTTCTCTCGCCCAGTTCGACCCAGCCGAGGATCGTTTTCAAGGGCTGCGCGTCGAGGTCGACATGCGTCAGCGTCCGC
+
BCCFFFFFHHDHHGHIJJJJJJJJJJJJJIHHHFFFFDEEEEDDDDDEDDDDDDDDDDEDD7CBDD@BD;BDDDDDDDDDDDDDDDDDDDDDDDDDD>BD@CCDCDDDDDDCDBBBDDDDDDDDBBD0?<9>3&4:>BB@<@B<@>9>

   usage:
   label_interleaved_fastq.py -i sequence.fastq 
   


---------------------------------------------------------------------------------------"""
#Header - Linkers, Libs, Constants
from string import strip
from Bio import SeqIO
from optparse import OptionParser

#---------------------------------------------------------------------------------------

#function declarations

def writeline_fastq(record, file):
    """write a single fastq record to a file"""   
    file.write(record.id + '\n')
    file.write(record.seq + '\n')
    file.write('+\n')
    file.write(record.letter_annotations + '\n')            

#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:	label_interleaved_fastq.py -i sequence.fastq ",                  
    description='9/18/14 JZL This script reads in an fastq file and fixes duplicate sequence names so a mate pair file can be generated.')
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
    infile = open(inputfilename,'U')      
    left, __, right = inputfilename.rpartition('.')
    outputfilename1 = left + '.1.' + right
    outputfilename2 = left + '.2.' + right
    
    parse_iterator = SeqIO.parse(infile, "fastq")
        
    print "Processing fasta read file...\n"        
    
    with open(inputfilename, 'U') as inputfile, open(outputfilename1, 'w') as out1, open(outputfilename2, 'w') as out2:
        oldrec = []
        old_mate = ''
        old_name = ''
        for record in parse_iterator:
            cur_mate = record.description.split(' ')[1][0]
            cur_name = record.name
            
            if cur_mate == '1' and old_mate == '1' and old_name == cur_name:
                record.description = record.description.split(' ')[0] + ' 2' + record.description.split(' ')[1][1:]
                out1.write(oldrec.format("fastq"))
                out2.write(record.format("fastq"))
            oldrec = record[:]
            old_mate = cur_mate[:]
            old_name = cur_name[:]
                
    print "Done!"
