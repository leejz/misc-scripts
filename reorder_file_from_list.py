#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 7/14/14
This script reads in a tab file and a text file of line headings and reorders 
all lines by the heading
   
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
   
--------------------------------------------------------------------------------   
usage:   reorder_file_from_list.py -i input.tab -f filter.txt
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants

import csv
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "reorder_file_from_list.py -i input.tab -s source.tab",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_tab", action="store", 
                        dest="inputfilename",
                        help="tab file of ordered list")
    parser.add_argument("-s", "--source_text", action="store", 
                        dest="sourcefilename",
                        help="source text file")
    options = parser.parse_args()

    mandatories = ["inputfilename", "sourcefilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
            
    inputfilename = options.inputfilename
    sourcefilename = options.sourcefilename
    left, __, right = sourcefilename.rpartition('.')
    
    print("Reading in source file...")
    with open(sourcefilename, 'U') as sourcefile:
        reader = csv.reader(sourcefile, dialect='excel-tab')    
        sourcelist = [line for line in reader]
        sourceheaders = [line[0] for line in sourcelist]
    
    print("Opening and parsing..."    )
    outputfilename = left +'.reordered.' + right        
    with open(inputfilename, 'U') as inputfile, open(outputfilename, 'w') as outfile:
        reader = csv.reader(inputfile, dialect='excel-tab')    
        writer = csv.writer(outfile, dialect='excel-tab')
        for headerline in reader:
            header = headerline[0]
            if header in sourceheaders:
                writer.writerow(sourcelist[sourceheaders.index(header)])
                del sourcelist[sourceheaders.index(header)]
                sourceheaders.remove(header)
            else:
                print("A heading was not found in the source file: " + header + ".  Exiting...")
                exit(-1) 
    print("Done!")
