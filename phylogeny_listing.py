#!/usr/bin/python
"""
11/21/11 JZL phylogeny_listing.py

This script reads a tab list file containing OTU taxonomy information, and a tab list file containing
OTU information and then outputs a tab list file with each sequence and taxonomy 
   
usage:
python phylogeny_listing.py -t OTU_tax.txt -u picked_otu.txt -o outfile.txt
   
OTU csv tab file format:
a tab-delimited file with each sequence and a semi-colon delimited string
NBB322_83       Bacteria;Firmicutes_Clostridia_1;Clostridiales;Lachnospiraceae;Catabacter;
NBB55_24        Bacteria;Firmicutes_Clostridia_1;Clostridiales;Ruminococcaceae;Anaerotruncus;
etc

OTU csv tab file format:
a tab-delimited file with each OTU number followed by OTU sequence members

0       NBB4_89 NBB4_93 NBB4_47
1       NBB22_75        NBB56_64        NBB2_70 NBB22_26        NBB76_80        2       NBB23_93
3       NBB24_02
4       NBB8_62
5       NBB322_13
6       NBB8_66
7       NBB22_24
8       NBB4_82 NBB4_49 NBB42C_12
etc

Output:
A tab-delimited file with each sequence and OTU listed   
NBB322_83       Bacteria;Firmicutes_Clostridia_1;Clostridiales;Lachnospiraceae;Catabacter;
NBB322_85       Bacteria;Firmicutes_Clostridia_1;Clostridiales;Lachnospiraceae;Catabacter;
NBB55_24        Bacteria;Firmicutes_Clostridia_1;Clostridiales;Ruminococcaceae;Anaerotruncus;
NBB67_21        Bacteria;Firmicutes_Clostridia_1;Clostridiales;Ruminococcaceae;Anaerotruncus;
etc

"""

"""------------------------------------------------------------------------------------------"""
"""Functions & Declarations"""

from string import strip
from numpy import *
import csv
import os as os
import random as random
from optparse import OptionParser

"""------------------------------------------------------------------------------------------"""
# Load files
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: phylogeny_listing.py -t OTU_tax.txt -u picked_otu.txt -o outfile.txt",
                  description='11/22/11 JZL phylogeny_listing.py')
    parser.add_option("-t", "--taxonomy_list", action="store", type="string", dest="taxfilename",
                  help="input tab delimited taxonomy file (see docstring)")
    parser.add_option("-u", "--OTU_list", action="store", type="string", dest="otufilename", 
                  help="input tab delimited OTU file (see docstring)")
    parser.add_option("-o", "--output_file", action="store", type="string", dest="outfilename", 
                  help="output tab delimited listing (see docstring)")
    (options, args) = parser.parse_args()

    mandatories = ["taxfilename", "otufilename","outfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nMissing parameter.  Must provide a filename.\n"
            parser.print_help()
            exit(-1)
    
    # read in command line args and parse file
    taxfilename = options.taxfilename
    otufilename = options.otufilename
    outfilename = options.outfilename
    taxfile = open(taxfilename, 'U')
    taxreader = csv.reader(taxfile, dialect='excel-tab')
    otufile = open(otufilename, 'U')
    otureader = csv.reader(otufile, dialect='excel-tab')
    
    otu_list = []
    for line in otureader:
        otu_list.append(line[1:])
    otufile.close()
    
    name_tax = []
    for line in taxreader:
        name_tax.append([line[0], line[1]])
    taxfile.close()
    #for each taxonomy, find the otu and write each sequence taxonomy line
    
    #open write file
    outfile = open(outfilename, 'wb')
    writer=csv.writer(outfile, dialect='excel-tab')
    
    #search and write
    for name_tax_entry in name_tax:
        print name_tax_entry
        for otu in otu_list:
            if name_tax_entry[0] in otu:
                for otu_member in otu:
                    writer.writerow([otu_member, name_tax_entry[1]])

    outfile.close()
    print 'Output file '+outfilename+' written.'

    
print "Done!"