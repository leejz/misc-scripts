#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
Jackson Lee 12/9/14
This script reads in a tab-delimited file and reports the top entry and % and outputs a 
text file of top matches

   Input file format:
   header\t   annotation\t
   
   Output
   header\t  top annotation\t   % of records
   
   usage:
   consensus_taxonomy.py -i in.file -o out.file


---------------------------------------------------------------------------------------"""
#Header - Linkers, Libs, Constants
from string import strip
from optparse import OptionParser
import pandas as pd
import csv

#function declarations

#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: consensus_taxonomy.py -i in.file -o out.file",                  
    description='12/9/14 This script reads in a tab-delimited file and reports the top entry \
and % and outputs a text file of top matches')
    parser.add_option("-i", "--input_file", action="store", type="string", dest="inputfilename",
                  help="text coverage file")
    parser.add_option("-m", "--mapping_file", action="store", type="string", dest="mappingfilename",
                  help="header\tbin mapping file (optional)", default='')
    parser.add_option("-o", "--output_file", action="store", type="string", dest="outputfilename",
                  help="text output file")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "outputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
            
    inputfilename = options.inputfilename
    mappingfilename = options.mappingfilename
    outputfilename = options.outputfilename
    
    if mappingfilename != '':
        with open(mappingfilename, 'U') as mappingfile:
            mapreader = csv.reader(mappingfile, dialect='excel-tab')
            mapping = {}
            for line in mapreader:
                if line[0] not in mapping:
                    mapping[line[0]] = line[1]
    
    #read in coverage file, the most complete record
    with open(inputfilename, 'U') as inputfile, open(outputfilename, 'w') as outputfile:
        binpd = pd.read_csv(inputfile, sep ='\t', header=True)
        binpd.columns = ["bin","annot"]
        if mappingfilename != '':
            binpd.bin = binpd.bin.str.split('_').str[0].map(mapping)
        binpd = binpd.dropna(axis=0)
        for bin in binpd.bin.unique():
            singlebinpd = binpd.loc[binpd.bin == bin,]
            valuecounts = singlebinpd.annot.value_counts()
            if valuecounts.index[0] != '-':
                topannotcount = valuecounts.iloc[0,]
                topannot = valuecounts.index[0]
            else:
                topannotcount = valuecounts.iloc[1,]
                topannot = valuecounts.index[1]
            topannotfreq = float(topannotcount) / len(singlebinpd.index)
            outputfile.write(str(bin) + '\t' + str(topannot) + '\t' + str(round(topannotfreq,2)) + '\n')
    print "Done!"
