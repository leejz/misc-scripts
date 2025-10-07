#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:  Jackson Lee 5/19/12
   
This script reads a tab-delimited QIIME OTU table containing abundance data and 
outputs a series of bootstrapped tables.  
   
otu table tab file format:
a qiime otu table, with the OTU name as first column, and name of the environment 
as the first row and the taxonomy in the last row.  
   
#Qiime 1.2.x OTU table
#OTU ID	Total	Ob.1	Ob.62Z	Scp.62	etc	Consensus Lineage
156	4	0	0	0	0	Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Bacteroidaceae;Bacteroides;unclassified;unclassified;unclassified
551	4	0	0	0	0	Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Bacteroidaceae;Bacteroides;unclassified;unclassified;unclassified
558	97	0	0	1	1	Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Bacteroidaceae;Bacteroides;unclassified;unclassified;unclassified
etc
   
outfile is in the same format
   
--------------------------------------------------------------------------------
usage:   bootstrap_generator.py -i qiime_otu_table.txt -o output_dir -b 100
"""

#-------------------------------------------------------------------------------
#Functions & Declarations
    
from string import strip
import os as os
import random as random
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "bootstrap_generator.py -i qiime_otu_table.\
txt -o output_directory -b 100",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--OTU table file", action="store", 
                        dest="infilename",
                        help="OTU table file (note: extention cannot be a number)")
    parser.add_argument("-o", "--output_dir", action="store", dest="outdirname",
                        help="new output directory")                  
    parser.add_argument("-b", "--bootstraps", action="store", type=int, 
                        dest="numbootstraps",
                        help="number of bootstraps")
    options = parser.parse_args()

    mandatories = ["infilename", "numbootstraps", "outdirname"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)

    # read in command line args and parse file
    infilename = options.infilename
    with open(infilename, 'U') as infile:    
        #read in header line
        firstline = infile.next()
        secondline = infile.next()
        #read in subsequent lines
        all_lines = [line.strip() in infile]
    
    #Bootstrap analysis.  Subsample with replacement bootstrap_n number of times, and generate
    #output files for each in a directory
    
    bootstrap_n = options.numbootstraps
    output_dir = './'+options.outdirname
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    else:
        print("\nError: Output directory already exists\n")
        parser.print_help()
        exit(-1)
    
    for i in range(bootstrap_n):
        bs_outfilename = output_dir+infilename+'.bs.%03d' % i +'.txt'
        with open(bs_outfilename, 'wb') as outfile:
            outfile.write(firstline)
            outfile.write(secondline)
            for replacement in range(len(all_lines)):
                outfile.write(random.choice(all_lines))
        print('Output file '+bs_outfilename+' written.')
    
print("Done!")
