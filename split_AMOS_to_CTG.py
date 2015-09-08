#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""split_AMOS_to_CTG.py"""
"""Jackson Lee 6/30/14"""
"""This script reads in an AMOS file and outputs the CTG section only for contig counting purposes.  
   This will reduce the file to ~10%
   
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
   
   usage:
   split_AMOS_to_CTG.py -i AMOS.afg
   
"""

"""---------------------------------------------------------------------------------------"""
"""Header - Linkers, Libs, Constants"""
from string import strip
from optparse import OptionParser

"""function declarations"""

"""---------------------------------------------------------------------------------------"""
"""Body"""
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    split_AMOS_to_CTG.py -i AMOS.afg",                  
    description='6/30/14 JZL split_AMOS_to_CTG.py. This script reads in an AMOS file and outputs the CTG section only for contig counting purposes. This will reduce the file to ~10%')
    parser.add_option("-i", "--input_fastq", action="store", type="string", dest="inputfilename",
                  help="AMOS alignment file")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)

    inputfilename = options.inputfilename
    outputfilename = inputfilename.rpartition('.')[0] + '.CTG_only.afg'
   
    print "Processing AMOS file...\n"    
 
    inputfile = open(inputfilename,'U')   
    outputfile = open(outputfilename,'w')   
    CTGflag = False
            
    for line in inputfile:
        if "{CTG" in line:
            CTGflag = True
        if CTGflag:
            outputfile.write(line)
    inputfile.close()
    outputfile.close()

    print "Done!"
