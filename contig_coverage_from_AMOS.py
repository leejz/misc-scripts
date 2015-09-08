#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""Jackson Lee 6/27/14"""
"""This script reads in an AMOS afg file and determines the list of contigs and reads associated.  It then output a coverage file and a contig to read mapping file, and a coverage file
   
   Input afg file format:
   {RED
   iid: internal ID
   eid: external ID, for Ray this is the sequence number
   Seq:
   ATGC...
   .
   qlt:
   DDDDDD...
   }
   {RED ...
   etc...
   }
   {CTG
   iid: internal count
   eid: contig name from file (for Ray)
   com:
   some software
   .
   seq:
   ATGC...
   .
   qlt:
   DDDDDD....
   .
   {TLE
   src: read iid
   off: offset in contig
   clr: order and gapping
   }
   {TLE
   etc...
   }
   }
   
   Input reflist of fastq file
   2402:1:1101:1392:2236/2
   2402:1:1101:1392:2237/2
   ... etc.
      
   Output mapping file format:
   contig-01\tread1\tread2\t etc...
   contig-02...etc.
   
   Output coverage file format:
   contig-01\tlength\tcount
   etc...
   
   usage:
   contig_coverage_from_AMOS.py -i AMOS.afg -o outfile.prefix
   
"""

"""---------------------------------------------------------------------------------------"""
"""Header - Linkers, Libs, Constants"""
from string import strip
import shelve
from optparse import OptionParser

"""function declarations"""

"""---------------------------------------------------------------------------------------"""
"""Body"""
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    contig_coverage_from_AMOS.py -i AMOS.afg -o outfile.prefix",                  
    description='6/27/14 JZL contig_coverage_from_AMOS.py reads in an AMOS afg file and determines the list of contigs and reads associated.  It then will read in a fastq file, and output a contig to read mapping file, and a coverage file')
    parser.add_option("-i", "--input_AMOS", action="store", type="string", dest="inputfilename",
                  help="fasta file of input sequences")
    """parser.add_option("-s", "--seqlist_db", action="store", type="string", dest="seqdbfilename",
                  help="sequence header file in shelve db format")"""
    parser.add_option("-o", "--output_prefix", action="store", type="string", dest="outputprefix",
                  help="prefix for set of output files")
    (options, args) = parser.parse_args()

    #mandatories = ["inputfilename", "seqdbfilename", "outputprefix"]
    mandatories = ["inputfilename", "outputprefix"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)

    #seqdbfilename = options.seqdbfilename
    inputfilename = options.inputfilename
    outputprefix = options.outputprefix
    outputcoveragefilename = outputprefix + '.coverage.txt'
    outputmappingfilename = outputprefix + '.read_contig_mapping.txt'
   
    """print "Reading in fastq read file...\n"    
 
    fastqinfile = open(fastqfilename,'U')   
    readdict = {}
    for fastqcount, sequence in enumerate(SeqIO.parse(fastqinfile, "fastq")):
        readdict[fastqcount+1] = sequence.id.strip()
    fastqinfile.close()
    
    inputfile = open(inputfilename,'U')
    linecount = 0
    for line in inputfile:
        linecount += 1
    inputfile.close() 
    """
    
    """print "Opening sequence reference db ...\n"
    
    header_db = shelve.open(seqdbfilename)
    """    
    
    print "Counting input file...\n"
    #line count file for last line capturing
    inputfile = open(inputfilename,'U')
    linecount = 0
    for line in inputfile:
        linecount += 1
    inputfile.close() 
    
    print "Extracting read mappings and writing coverage and mapping files\n"

    inputfile = open(inputfilename,'U')
    outputcoveragefile = open(outputcoveragefilename, 'w')
    outputmappingfile = open(outputmappingfilename, 'w')

    block = []
            
    for i, line in enumerate(inputfile):
        if "{CTG" in line or i == linecount-1:
            contigflag = False
            for blockline in block:
                if "{CTG" in blockline:
                    contigflag = True
                    TLEflag = False   
                    seqflag = False     
                    seqlen = 0            
                    eid = ''
                    readlist = []
                if contigflag:
                    if seqflag:
                        seqlen = len(blockline)
                        seqflag = False
                    if "seq:" in blockline:
                        seqflag = True
                    if "eid:" in blockline:
                        eid = blockline.rpartition("eid:")[2]
                    if "{TLE" in blockline:
                        TLEflag = True
                    if TLEflag and "src:" in blockline:
                        readlist.append(blockline.rpartition("src:")[2])
                        TLEflag = False
            if contigflag:
                outputcoveragefile.write(eid + "\t" + str(len(readlist)) + "\t" + str(seqlen) + "\n")
                #outputmappingfile.write(eid + "\t" + "\t".join(header_db[str(key-1)] for key in readlist) + "\n")
                outputmappingfile.write(eid + "\t" + "\t".join(key for key in readlist) + "\n")
            block = []
        block.append(line.strip())
                    
    inputfile.close()
    outputcoveragefile.close()
    outputmappingfile.close()

    print "Done!"
