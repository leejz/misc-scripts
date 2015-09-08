#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""reorder_file_from_list.py"""
"""Jackson Lee 7/14/14"""
"""This script reads in a tab file and a text file of line headings and reorders all lines by the heading
   
   Input  file format:
   1\t1\t1\t2\t
   etc
   

   Input filter file format:
   one number per line matching the sequence order number in order. 0 being first
   
   0
   5
   10 
   22
   etc.
   
   Output file format:
   same as input file
   
   usage:
   reorder_file_from_list.py -i input.tab -f filter.txt
"""

"""---------------------------------------------------------------------------------------"""
"""Header - Linkers, Libs, Constants"""
from string import strip
import csv
from optparse import OptionParser


"""---------------------------------------------------------------------------------------"""

"""function declarations"""

"""---------------------------------------------------------------------------------------"""

"""Body"""
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    reorder_file_from_list.py -i input.tab -s source.tab",                  
    description='7/14/14 JZL reorder_file_from_list.py  This script reads in a tab file and a text file of line headings and filters all lines by the heading')
    parser.add_option("-i", "--input_tab", action="store", type="string", dest="inputfilename",
                  help="tab file of ordered list")
    parser.add_option("-s", "--source_text", action="store", type="string", dest="sourcefilename",
                  help="source text file")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "sourcefilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
            
    inputfilename = options.inputfilename
    sourcefilename = options.sourcefilename
    left, __, right = sourcefilename.rpartition('.')
    
    print "Reading in source file..."
    sourcefile = open(sourcefilename, 'U') 
    reader = csv.reader(sourcefile, dialect='excel-tab')    
    sourcelist = [line for line in reader]
    sourceheaders = [line[0] for line in sourcelist]
    sourcefile.close()
    
    inputfile = open(inputfilename, 'U')
    outputfilename = left +'.reordered.' + right        
    outfile = open(outputfilename, 'w')
                                    
    print "Opening and parsing..."    
    reader = csv.reader(inputfile, dialect='excel-tab')    
    writer = csv.writer(outfile, dialect='excel-tab')
    for headerline in reader:
        header = headerline[0]
        if header in sourceheaders:
            writer.writerow(sourcelist[sourceheaders.index(header)])
            del sourcelist[sourceheaders.index(header)]
            sourceheaders.remove(header)
        else:
            print "A heading was not found in the source file: " + header + ".  Exiting..."
            exit(-1) 
    inputfile.close()
    outfile.close()
    print "Done!"
