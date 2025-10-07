#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 12/20/11

This script reads a name list file containing sequence names and a file 
containing taxonomy information, and then outputs a taxonomy file with the named 
sequences removed.
      
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

--------------------------------------------------------------------------------
usage:    python -n names.txt -t classified.taxonomy
"""

#-------------------------------------------------------------------------------

#Header - Linkers, Libs, Constants
from string import strip
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "python -n names.txt -t classified.taxonomy.txt",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-n", "--name", action="store", dest="namefilename",
                  help="txt file of list of names")
    parser.add_argument("-t", "--tax", action="store", dest="taxfilename",
                  help="space-delimited taxonomy file")
    options = parser.parse_args()

    mandatories = ["namefilename", "taxfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)    
    # read in command line args and parse file
    
    with open(namefilename, 'U') as namefile:
        remove_names = [line.strip() for line in namefile]
        
    outfilename = taxfilename.split('taxonomy')[0]+'filtered.taxonomy'

    with open(outfilename, 'wb') as outfile, open(taxfilename, 'U') as taxfile:
        #read in each line of each file
        for line in taxfile:
            #parse each line
            taxname, space, tax = line.strip().partition(' ')
            if taxname not in remove_names:
                 outfile.write(line)

        print('Output file '+outfilename+' written.')

    
print("Done!")
