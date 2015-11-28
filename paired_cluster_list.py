#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 7/1/14
This script converts a single filter readlist to a paired readlist. This script
is used in AMOS Ray cluster file filtering.

Input cluster file format:
readindex
readindex
offsetindex
offsetreadindex
offsetreadindex
   
   
Output
readindex1
readindex2
offsetindex
offsetreadindex1 - offsetindex
offsetreadindex2 - offsetindex
etc...

--------------------------------------------------------------------------------   
usage:   paired_cluster_list.py -i listofreads.txt -p lastline.interger -o outputfilename
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
"""Body"""
print "Running..."

if __name__ == '__main__':
    parser = ArgumentParser(usage = "paired_cluster_list.py -i listofreads.txt \
-p lastline.integer -o outputfilename",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--linenum_file", action="store", 
                        dest="linenumfilename",
                        help="list of sequential reads from a paired file")
    parser.add_argument("-p", "--paired_index", action="store", type=int, 
                        dest="pairedindex",
                        help="last line index to split file", default = 0)
    parser.add_argument("-o", "--output_file", action="store", 
                        dest="outputfilename", help="text output file")
    options = parser.parse_args()

    mandatories = ["linenumfilename", "pairedindex", "outputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
            
    linenumfilename = options.linenumfilename
    pairedindex = options.pairedindex
    outputfilename = options.outputfilename
    
    print "Read in linenum file..."
    with open(linenumfilename, 'U') as linenumfile:
        readnum_list = [int(linenum.strip()) for linenum in linenumfile]
            
    print "Combining forward and reverse read lists..."
    
    forward_list = [linenum for linenum in readnum_list if linenum <= options.pairedindex]
    reverse_list = [linenum - pairedindex for linenum in readnum_list if linenum > options.pairedindex]
    pairednum_list = forward_list + reverse_list
    pairednum_list = list(set(pairednum_list))
    pairednum_list.sort()	
        
    print "Writing " + outputfilename
    with open(outputfilename, 'w') as outputfile:
        for readnum in pairednum_list:
            outputfile.write(str(readnum)+"\n")
        
    print "Done!"
