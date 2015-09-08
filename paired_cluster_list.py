#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""paired_cluster_list.py"""
"""Jackson Lee 7/1/14"""
"""This script converts a single filter readlist to a paired readlist

   Input cluster file format:
   header\t   number\tnumber
   
   Input filter file format:
   contig-01
   contig-02
   etc...
   
   Output
   number
   number
   etc...
   
   usage:
   paired_cluster_list.py -i listofreads.txt -p lastline.interger -o outputfilename
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
    parser = OptionParser(usage = "usage: paired_cluster_list.py -i listofreads.txt -p lastline.integer -o outputfilename",                  
    description='JZL 7/1/14 This script converts a single filter readlist to a paired readlist.')
    parser.add_option("-i", "--linenum_file", action="store", type="string", dest="linenumfilename",
                  help="list of sequential reads from a paired file")
    parser.add_option("-p", "--paired_index", action="store", type="int", dest="pairedindex",
                  help="last line index to split file", default = 0)
    parser.add_option("-o", "--output_file", action="store", type="string", dest="outputfilename",
                  help="text output file")
    (options, args) = parser.parse_args()

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
    linenumfile = open(linenumfilename, 'U')
    readnum_list = [int(linenum.strip()) for linenum in linenumfile]
    linenumfile.close()
            
    print "Combining forward and reverse read lists..."
    
    forward_list = [linenum for linenum in readnum_list if linenum <= options.pairedindex]
    reverse_list = [linenum - pairedindex for linenum in readnum_list if linenum > options.pairedindex]
    pairednum_list = forward_list + reverse_list
    pairednum_list = list(set(pairednum_list))
    pairednum_list.sort()	
        
    print "Writing " + outputfilename
    outputfile = open(outputfilename, 'w')
    for readnum in pairednum_list:
        outputfile.write(str(readnum)+"\n")
    outputfile.close()
        
    print "Done!"
