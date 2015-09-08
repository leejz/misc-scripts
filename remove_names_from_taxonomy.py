#!/usr/bin/python
"""
12/20/11 JZL remove_names_from_taxonomy.py

This script reads a name list file containing sequence names and a file containing taxonomy information, 
and then outputs a taxonomy file with the named sequences removed.
   
usage:
python names.txt classified.taxonomy
   
names list format:
NBB322_83
NBB55_24
etc

taxonomy format:
a space-delimited file with each OTU number followed by OTU sequence members

NBB322_83 Bacteria;Firmicutes_Clostridia_1;Clostridiales;Lachnospiraceae;Catabacter;
NBB322_85 Bacteria;Firmicutes_Clostridia_1;Clostridiales;Lachnospiraceae;Catabacter;
NBB55_24 Bacteria;Firmicutes_Clostridia_1;Clostridiales;Ruminococcaceae;Anaerotruncus;
NBB67_21 Bacteria;Firmicutes_Clostridia_1;Clostridiales;Ruminococcaceae;Anaerotruncus;
etc

Output:
same taxonomy format
"""

"""------------------------------------------------------------------------------------------"""
"""Functions & Declarations"""

from string import strip
import os as os


"""------------------------------------------------------------------------------------------"""
# Load files
print "Running..."

if __name__ == '__main__':
    from sys import argv
    
    # read in command line args and parse file
    namefilename = argv[-2]
    namefile = open(namefilename, 'U')
    taxfilename = argv[-1]
    taxfile = open(taxfilename, 'U')
    
    remove_names = []
    for line in namefile:
        remove_names.append(line.strip())
        
    outfilename = taxfilename.split('taxonomy')[0]+'filtered.taxonomy'
    outfile = open(outfilename, 'wb')
    
    #read in each line of each file
    for line in taxfile:
        #parse each line
        taxname, space, tax = line.strip().partition(' ')
        if taxname not in remove_names:
            outfile.write(line)
    outfile.close()
    print 'Output file '+outfilename+' written.'

    
print "Done!"