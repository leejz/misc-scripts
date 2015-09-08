#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
filter_line_by_linenum.py
Jackson Lee 7/14/14
This script reads in a tab file and a text file of line headings and filters all lines by the heading
   
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
   filter_line_by_list.py -i input.tab -f filter.txt


---------------------------------------------------------------------------------------"""
#Header - Linkers, Libs, Constants
from string import strip
import csv
from optparse import OptionParser


#---------------------------------------------------------------------------------------

#function declarations

#---------------------------------------------------------------------------------------

#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    filter_line_by_linenum.py -i input.tab -f filter.txt",                  
    description='7/14/14 JZL filter_line_by_list.py.  This script reads in a tab file and a text file of line headings and filters all lines by the heading (See DocString)')
    parser.add_option("-i", "--input_tab", action="store", type="string", dest="inputfilename",
                  help="tab file")
    parser.add_option("-f", "--filter_text", action="store", type="string", dest="filterfilename",
                  help="filter text file")
    parser.add_option("-r", "--reverse_filter_flag", action="store_true", dest="reverseflag", default=False,
                  help="set to enable exclusion filtering")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "filterfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
            
    inputfilename = options.inputfilename
    filterfilename = options.filterfilename
    left, __, right = inputfilename.rpartition('.')
    
    print "Reading in filter file..."
    filterfile = open(filterfilename, 'U') 
    filterlist = [line.strip() for line in filterfile]
    filterfile.close()
    
    inputfile = open(inputfilename, 'U')
                    
    print "Opening and parsing..."
    if options.reverseflag:        
        print "Exclusion filtering enabled.  Saving lines not in " + filterfilename 
        outputfilename = left +'.exclusion.filtered.' + right        
        outfile = open(outputfilename, 'w')
        reader = csv.reader(inputfile, dialect='excel-tab')
        writer = csv.writer(outfile, dialect='excel-tab')
        for line in reader:
            if not(line[0] in filterlist):
                writer.writerow(line)
    else:
        outputfilename = left +'.filtered.' + right        
        outfile = open(outputfilename, 'w')
        reader = csv.reader(inputfile, dialect='excel-tab')
        writer = csv.writer(outfile, dialect='excel-tab')
        for line in reader:
            if line[0] in filterlist:
                writer.writerow(line)
            
    inputfile.close()
    outfile.close()
    print "Done!"
