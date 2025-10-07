#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:  Jackson Lee 7/1/14
This script reads in a tab delimited file of numbers and clusters, and a filter 
file of cluster names. Then the script will extract the numbers, order them, and 
write to disk.  This script can take in several filter files at once. This script
is used in AMOS file Ray filtering.

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
   
--------------------------------------------------------------------------------
usage:   flatten_cluster_list.py -i clusterlist.tab -f filterlist.txt -o outputfilename
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import csv

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "flatten_cluster_list.py -i clusterlist.tab \
-f filterlist.txt -o outputfilename",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--clusterlist_file", action="store", 
                        dest="clusterfilename",
                        help="tab-delimited cluster list file")
    parser.add_argument("-f", "--filter_file", action="store", 
                        dest="filterfilename",
                        help="text filter file")
    parser.add_argument("-p", "--paired", action="store_true",  
                        dest="pairedindex", 
                        help="paired index length (paired mode ON)")
    parser.add_argument("-o", "--output_file", action="store", 
                        dest="outputfilename", help="text output file")
    options = parser.parse_args()

    mandatories = ["clusterfilename", "filterfilename", "outputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
            
    clusterfilename = options.clusterfilename
    filterfilename = options.filterfilename
    outputfilename = options.outputfilename
    
    print("Read in filter file...")
    with open(filterfilename, 'U') as filterfile:
        filterlines = [filterline.strip() for filterline in filterfile]
            
    print("Matching records and flattening...")
    #read in coverage file, the most complete record
    with open(clusterfilename, 'U') as clusterfile:
        reader = csv.reader(clusterfile, dialect='excel-tab')

        readnum_list = []
        for cluster in reader:
            if cluster[0] in filterlines:
                readnum_list+= map(int, cluster[1:])

    readnum_list = list(set(readnum_list))
    readnum_list.sort()

    if options.pairedindex:
        print("Paired read mode detected, combining forward and reverse read lists\n")
        forward_list = [linenum for linenum in readnum_list if linenum <= pairedindex]
        reverse_list = [linenum - pairedindex for linenum in readnum_list if linenum < pairedindex]
        pairednum_list = forward_list + reverse_list
        pairednum_list = list(set(pairednum_list))
        pairednum_list.sort()
        readnum_list = pairednum_list
        
    print("Writing " + outputfilename)
    with open(outputfilename, 'w') as outputfile:
        for readnum in readnum_list:
            outputfile.write(str(readnum)+"\n")
        
    print("Done!")
