#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
Jackson Lee 1/16/15
This script reads in a integrated metastranscriptomics mapping file and a file of duplicate reads
and combines the duplicate records.  It combines the annotations, if they are identical, and appends
if they are not.  It sums each RPKM value for each library as well.

   Input file format:
   database format:
   header	bin_num	function	ontology	organism	taxonomy	Sample_name_RPKM	etc.
   scaffold-0_42	1	InsA-like protein	glutathione S-transferase [EC:2.5.1.18]|K00799	Lyngbya sp. PCC 8106	Bacteria;Cyanobacteria;unclassified (derived from Cyanobacteria);Oscillatoriales;unclassified (derived from Oscillatoriales);Lyngbya;Lyngbya sp. PCC 8106;Lyngbya sp. PCC 8106	105.2
   ...
   
   usage:
   sum_duplicate_mappings.py -i mt.tab -f cluster.txt -o out.tab

---------------------------------------------------------------------------------------"""
#Header - Linkers, Libs, Constants
from string import strip
from optparse import OptionParser
import csv
import pandas as pd

#function declarations

#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: sum_duplicate_mappings.py -i mt.tab -f cluster.txt -o out.tab",                  
    description="JZL 1/16/15 This script reads in a integrated metastranscriptomics mapping file and a file of \
duplicate reads and combines the duplicate records.  It combines the annotations, if they are identical, \
and appends if they are not.  It sums each RPKM value for each library as well.")
    parser.add_option("-i", "--input_filename", action="store", type="string", dest="inputfilename",
                  help="input tab delimited data file")
    parser.add_option("-f", "--duplicates_filename", action="store", type="string", dest="dupfilename",
                  help="output tab delimited data file")                  
    parser.add_option("-o", "--output_filename", action="store", type="string", dest="outputfilename",
                  help="output tab delimited data file")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "dupfilename", "outputfilename"]
    
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)

    inputfilename = options.inputfilename
    outputfilename = options.outputfilename
    dupfilename = options.dupfilename
        
    with open(inputfilename,'U') as infile:
        #combined = pd.read_csv(infile, header=0, sep='\t')
        datareader = csv.reader(infile, dialect='excel-tab')
        firstrow = datareader.next()
        data = {}
        for datalist in datareader:
            data[datalist[0]] = datalist

    #combined.columns = ["header", "bin_num", "function", "ontology", "organism", "taxonomy"] + combined.columns.tolist()[6:]
    #combinedheaders = combined.header.tolist()
    
    with open(dupfilename, 'U') as dupfile:
        dupreader = csv.reader(dupfile, dialect='excel-tab')
        for duplist in dupreader:
            #live_duplist = [dup for dup in duplist if dup in combinedheaders]
            datakeys = data.keys()
            live_duplist = [dup for dup in duplist if dup in datakeys]
            if len(live_duplist) > 1:
                dupdata = [data.pop(dup) for dup in live_duplist]                
                dupannots = [dup[1:6] for dup in dupdata]
                dupcounts = [dup[6:] for dup in dupdata]
                newdictentry = []
                newkey = 'x'.join([dup[0] for dup in dupdata])
                newdictentry.append(newkey)
                for newset in zip(*dupannots):
                    newdictentry.append('-x-'.join(map(str,[unique for unique in set(newset) if unique != ''])))
                for newset in zip(*dupcounts):
                    newdictentry.append(sum(map(float,newset)))                
                data[newkey] = newdictentry
                if len(data) % 10 == 0:
                    print len(data), ' entries'
                            
                #dupframe = combined[combined.header.isin(live_duplist)]
                #combined = combined.drop(dupframe.index)
                #newrowheader = 'x'.join(dupframe.header.tolist())
                #temp = []
                #for index in range(len(dupframe.columns)): # this is so unphythonic
                #    if index == 0:
                #        temp.append(newrowheader)
                #    elif index > 0 and index < 6:
                #        temp.append('-x-'.join(map(str,dupframe.iloc[:,index].dropna().unique().tolist())))
                #    elif index >= 6:
                #        temp.append(dupframe.iloc[:,index].sum())
                #combined.loc[combined.index[-1]+1] = pd.Series(temp,index=combined.columns)
    
    print "Writing ..."
    with open(outputfilename, 'w') as outfile:
        #combined.to_csv(outfile, sep="\t", header=True, index=False)
        writer = csv.writer(outfile, dialect = 'excel-tab')
        writer.writerow(firstrow)
        datavals = data.values()
        datavals.sort(key=lambda x: x[1])
        for valuelist in datavals:
            writer.writerow(valuelist)
                
    print "Done!"
