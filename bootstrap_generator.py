#!/usr/bin/python
"""5/19/12 JZL bootstrap_generator.py
   
   This script reads a tab file containing abundance data and outputs a series of bootstrapped tables.  
   
   usage:
   python bootstrap_generator.py -i qiime_otu_table.txt -o output_dir -b 100
   
   otu table tab file format:
   a qiime otu table, with the OTU name as first column, and name of the environment as the first 
   row and the taxonomy in the last row.  
   
   #Qiime 1.2.x OTU table
   #OTU ID	Total	Ob.1	Ob.62Z	Scp.62	etc	Consensus Lineage
   156	4	0	0	0	0	Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Bacteroidaceae;Bacteroides;unclassified;unclassified;unclassified
   551	4	0	0	0	0	Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Bacteroidaceae;Bacteroides;unclassified;unclassified;unclassified
   558	97	0	0	1	1	Bacteria;Bacteroidetes;Bacteroidia;Bacteroidales;Bacteroidaceae;Bacteroides;unclassified;unclassified;unclassified
   etc
   
   outfile is in the same format
   """
"""------------------------------------------------------------------------------------------"""
"""Functions & Declarations"""
    
from string import strip
import os as os
import random as random
from optparse import OptionParser

"""------------------------------------------------------------------------------------------"""
# Load files
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:       python bootstrap_generator.py -i qiime_otu_table.txt -o output_directory -b 100",                  
    description='5/19/12 JZL bootstrap_generator.py.  Read in a QIIME OTU table and output a series of bootstrapped tables in a directory')
    parser.add_option("-i", "--OTU table file", action="store", type="string", dest="infilename",
                  help="OTU table file (note: extention cannot be a number)")
    parser.add_option("-o", "--output_dir", action="store", type="string", dest="outdirname",
                  help="new output directory")                  
    parser.add_option("-b", "--bootstraps", action="store", type="int", dest="numbootstraps",
                  help="number of bootstraps")
    (options, args) = parser.parse_args()

    mandatories = ["infilename", "numbootstraps", "outdirname"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)

    # read in command line args and parse file
    infilename = options.infilename
    infile = open(infilename, 'U')
    
    #read in header line
    firstline = infile.next()
    secondline = infile.next()
    all_lines=[]
    #read in subsequent lines
    for line in infile:
        all_lines.append(line)
    infile.close()
    
    #Bootstrap analysis.  Subsample with replacement bootstrap_n number of times, and generate
    #output files for each in a directory
    
    bootstrap_n = options.numbootstraps
    output_dir = './'+options.outdirname
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    else:
        print "\nError: Output directory already exists\n"
        parser.print_help()
        exit(-1)
    
    for i in range(bootstrap_n):
        bs_outfilename = output_dir+infilename+'.bs.%03d' % i +'.txt'
        outfile = open(bs_outfilename, 'wb')
        outfile.write(firstline)
        outfile.write(secondline)
    
        for replacement in range(len(all_lines)):
            outfile.write(random.choice(all_lines))
        outfile.close()
    
        print 'Output file '+bs_outfilename+' written.'
    
print "Done!"