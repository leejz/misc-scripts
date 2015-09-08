#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""split_cluster_list.py"""
"""Jackson Lee 7/8/14"""
"""This script reads in a tab delimited file of clusters, and a list of number ranges for reads in
   each cluster.  The script will parse all reads based on the number ranges, and then output a file for each range.

   Input cluster file format:
   header\t   number\tnumber
   etc...
   
   Input list format:
   number,number,number   
   etc...

   mapping file
   list of master reads in order of filtered reads (from flatten_cluster_list.py)
   Output
   one cluster list file for each number range
      
   usage:
   split_cluster_list.py -i clusterlist.tab -f number1,number2,number3 -m mapping.list.txt
"""

"""---------------------------------------------------------------------------------------"""
"""Header - Linkers, Libs, Constants"""
from string import strip
from bisect import bisect_left
from optparse import OptionParser
import csv

"""function declarations"""

"""---------------------------------------------------------------------------------------"""
"""Body"""
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: split_cluster_list.py -i clusterlist.tab -f number1,number2,number3 -m mapping.list.txt (optional)",                  
    description='JZL 7/8/14 This script reads in a tab delimited file of clusters, and a list of number ranges for reads in each cluster.  The script will parse all reads based on the number ranges, and then output a file for each range.')
    parser.add_option("-i", "--clusterlist_file", action="store", type="string", dest="clusterfilename",
                  help="tab-delimited cluster list file")
    parser.add_option("-f", "--filter_list", action="store", type="string", dest="filterlist",
                  help="comma separated list of filter indices delimiting ranges")
    parser.add_option("-m", "--mapping_file", action="store", type="string", dest="mappingfilename",
                  help="single line list of mapping reads (optional)")
    (options, args) = parser.parse_args()

    mandatories = ["clusterfilename", "filterlist"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
                        
    clusterfilename = options.clusterfilename
    left, __, right = clusterfilename.rpartition('.')
    filterlist = map(int, options.filterlist.strip().split(","))
    filterlist.sort()
    
    mappingflag = False
    if options.mappingfilename != None:        
        print "Mapping file detected.  Reading file."
        mappingflag = True
        with open(options.mappingfilename, 'U') as mappingfile:
            mapping_list = [int(line.strip()) for line in mappingfile]

    print "Matching records and parsing..."
    
    clusterfile = open(clusterfilename, 'U')
    reader = csv.reader(clusterfile, dialect='excel-tab')
    outputfilename = left + ".parsed." + right

    with open(outputfilename, 'w') as outputfile:    
        outputfilewriter = csv.writer(outputfile, dialect='excel-tab')
        for line in reader:
            output_counter = [0 for i in filterlist]
            for readnum in line[1:]:
                if readnum != '':
                    if mappingflag:
                        if int(readnum) < len(mapping_list):
                            output_counter[bisect_left(filterlist, mapping_list[int(readnum)])-1] +=1
                        else:
                            output_counter[-1] +=1
                    else:
                        output_counter[bisect_left(filterlist, int(readnum))-1] +=1                
            outputfilewriter.writerow([line[0]] + map(str, output_counter))
    clusterfile.close()
    print "Done!"
