#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:  Jackson Lee 7/14/14

This script reads in a tab file and a text file of line headings and filters all 
lines by the heading
   
Input  file format:
1\t1\t1\t2\t
etc
   
Input filter file format:
>header name 1

or 

header name 1
etc...
   
Output file format:
same as input file

--------------------------------------------------------------------------------   
usage:   filter_line_by_list.py -i input.tab -f filter.txt
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
    parser = ArgumentParser(usage = "filter_line_by_linenum.py -i input.tab -f \
filter.txt",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_tab", action="store",
                        dest="inputfilename", help="tab file")
    parser.add_argument("-f", "--filter_text", action="store", 
                        dest="filterfilename", help="filter text file")
    parser.add_argument("-r", "--reverse_filter_flag", action="store_true", 
                        dest="reverseflag", help="set to enable exclusion filtering")
    options = parser.parse_args()

    mandatories = ["inputfilename", "filterfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
            
    inputfilename = options.inputfilename
    filterfilename = options.filterfilename
    left, __, right = inputfilename.rpartition('.')
    
    print("Reading in filter file...")
    with open(filterfilename, 'U') as filterfile:
        filterlist = [line.strip() for line in filterfile]
    
    with open(inputfilename, 'U')as inputfile:                    
        print("Opening and parsing...")
        if options.reverseflag:        
            print("Exclusion filtering enabled.  Saving lines not in " + filterfilename )
            outputfilename = left +'.exclusion.filtered.' + right        
            with open(outputfilename, 'w') as outfile:
                reader = csv.reader(inputfile, dialect='excel-tab')
                writer = csv.writer(outfile, dialect='excel-tab')
                for line in reader:
                    if not(line[0] in filterlist):
                        writer.writerow(line)
        else:
            outputfilename = left +'.filtered.' + right        
            with open(outputfilename, 'w') as outfile:
                reader = csv.reader(inputfile, dialect='excel-tab')
                writer = csv.writer(outfile, dialect='excel-tab')
                for line in reader:
                    if line[0] in filterlist:
                        writer.writerow(line)
            
    print("Done!")
