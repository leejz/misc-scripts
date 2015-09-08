#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
Jackson Lee 9/24/14
This script reads in an per base bedtools gff, the source gff file, and then calculates 
the length and average coverage depth of each feature.  It also concats start stop positions 
for creating unique names
   
      bedtools coverage output: Output (tab delimited) after each base of each feature in B:

    1) depth
    2) # bases at depth

   Input per base gff (coverage output)
contig-100000014	FIG	CDS	15388	17094	.	+	1	ID=fig|6666666.84680.peg.14;Name=Tungsten-containing aldehyde:ferredoxin oxidoreductase (EC 1.2.7.5);Ontology_term=KEGG_ENZYME:1.2.7.5	1	60
contig-100000014	FIG	CDS	15388	17094	.	+	1	ID=fig|6666666.84680.peg.14;Name=Tungsten-containing aldehyde:ferredoxin oxidoreductase (EC 1.2.7.5);Ontology_term=KEGG_ENZYME:1.2.7.5	2	60
contig-100000014	FIG	CDS	15388	17094	.	+	1	ID=fig|6666666.84680.peg.14;Name=Tungsten-containing aldehyde:ferredoxin oxidoreductase (EC 1.2.7.5);Ontology_term=KEGG_ENZYME:1.2.7.5	3	60
contig-100000014	FIG	CDS	15388	17094	.	+	1	ID=fig|6666666.84680.peg.14;Name=Tungsten-containing aldehyde:ferredoxin oxidoreductase (EC 1.2.7.5);Ontology_term=KEGG_ENZYME:1.2.7.5	4	64

  Input per base txt (genomcov output)
contig-100000014	1	60  
contig-100000014	2	60  
contig-100000014	3	60  
  
   Output coverage file format:
   contig-01\tlength\taverage coverage
   etc...
   
   usage:
   contig_coverage_from_perbase_gff.py -i perbase.gff -t -o outfile.file
   


---------------------------------------------------------------------------------------"""
#Header - Linkers, Libs, Constants
from string import strip
from numpy import mean
from optparse import OptionParser
from itertools import islice
import csv

#function declarations

#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    contig_coverage_from_perbase_gff.py -i perbase.gff -t -o outfile.file",                  
    description='9/24/14 JZL This script reads in an per base bedtools gff, the source gff file, and then calculates the length and average coverage depth of each feature.  It also concats start stop positions for creating unique names')
    parser.add_option("-i", "--perbase_gff", action="store", type="string", dest="inputfilename",
                  help="perbase (bedtools coverage -d) gff file")
    parser.add_option("-t", "--perbase_txt", action="store_true", default=False, dest="tabflag",
                  help="set True to use perbase genome (bedtools genomecov -d) txt file")
    parser.add_option("-o", "--output_file", action="store", type="string", dest="outputfilename",
                  help="output coverage file name")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "outputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)

    inputfilename = options.inputfilename
    outputfilename = options.outputfilename
    
    print "Calculating per base coverages..."
    if options.tabflag:
        with open(inputfilename, 'U') as inputfile:
            parse_dict = {}
            orderlist = []
            for line in inputfile:  
                parsedline = line.strip().split('\t')
                featurename = parsedline[0]
                cov = parsedline[-1]
                if featurename in parse_dict:
                    parse_dict[featurename].append(cov)
                else:
                    parse_dict[featurename] = [cov]                        
                    orderlist.append(featurename)

        with open(outputfilename, 'w') as outputfile:          
            writer = csv.writer(outputfile, dialect='excel-tab')                    
            for entry in orderlist:
                featurename = entry
                seqlen = len(parse_dict[entry])
                avgcov = mean(map(int,parse_dict[entry]))
                writer.writerow([featurename, seqlen, avgcov])    

    else:        
        with open(outputfilename, 'w') as outputfile:
            writer = csv.writer(outputfile, dialect='excel-tab')
            with open(inputfilename, 'U') as inputfile:
                for line in inputfile:  
                    parsedline = line.strip().split('\t')
                    featurename = parsedline[0] + '_' + parsedline[3] + '_' + parsedline[4]
                    seqlen = int(parsedline[4])-int(parsedline[3])
                    countlist = [parsedline[-1]]
                    for countline in islice(inputfile,seqlen):
                        countlist.append(countline.strip().split('\t')[-1])
                    avgcov = mean(map(int,countlist))
                    writer.writerow([featurename, seqlen, avgcov])
                    
    print "Done!"
