#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
Jackson Lee 1/19/15

This script reads in a combined database data format file and a search file to determine functional
gene statistics.  

   Input file format:
   database format:
   header	bin_num	function	ontology	organism	taxonomy	Sample_name_RPKM	etc.
   scaffold-0_42	1	InsA-like protein	glutathione S-transferase [EC:2.5.1.18]|K00799	Lyngbya sp. PCC 8106	Bacteria;Cyanobacteria;unclassified (derived from Cyanobacteria);Oscillatoriales;unclassified (derived from Oscillatoriales);Lyngbya;Lyngbya sp. PCC 8106;Lyngbya sp. PCC 8106	105.2
   ...

   Query file tab-delimited format:
   abbreviation	name	chain or subunit	code	subunit	EC	exclude	nested
   DSR	dissimilatory sulfite reductase;sulfite reductase, dissimilatory-type	alpha;beta;A;B	dsr	AB	1.8.99.1		
   
   Search pseudocode:
   1. If EC code field is there, set fields with EC as False.  
         If no EC field, skip step.
         If EC match found, Set 'maybe'.  
         If 'maybe', check if query chain or subunit exists.
            If either query chain or field exists, search for chain or field match.  
            If either field matches, set True
         If no query field exists, set 'maybe' to True

   2. If 3 digit code field is there, check for matches of the remaining:
         If there is no subunit, check only for code
            If code matches, set True
         If subunit field exists, check for subunit and code match
            If subunit and code matches, set True

   3. If name field is there, check for name matches of the remaining:
         Set all remainder to False
         If name whole word matches, check if chain exists.
            If chain field matches, set True.
            If chain field mismatch, set False
         If no chain field exists, set True
         If nested field is there, 
             for each nested item, 
                 search for named hits and set True if matched
                 set original field to false for all matches
                 create a new abbreviation code and field from these
                                                 
   4. If anything in exclude column matches in search column, set False
      
    If a match is found, the data is saved and subdivided by bin.  The ratio is calculated 
    with the bin median log2 (RPKM gene / bin RPKM median). This is done for all timepoints
    and the median taken over timepoints. The duplicates are averaged.
    
    Several tables are output.  The table of bins vs. abbreviations, with averaged medians.  And
    a table of gene counts.  This script also outputs a directory of search results.    
    
   usage:
   search_combined_data.py -i data.file -q query.tab -o out.prefix

---------------------------------------------------------------------------------------"""
#Header - Linkers, Libs, Constants
from string import strip
from optparse import OptionParser
import csv
import os
import pandas as pd
import numpy as np	

#function declarations

#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: calculate_bin_stats.py -i data.file -o out.file",                  
    description="JZL 1/19/15 This script reads in a combined database data format file and a \
search file to determine functional gene statistics.  See the DocString for file formats and search methodology.")
    parser.add_option("-i", "--input_filename", action="store", type="string", dest="inputfilename",
                  help="input tab delimited data file")
    parser.add_option("-q", "--query_filename", action="store", type="string", dest="queryfilename",
                  help="query tab delimited data file")
    parser.add_option("-o", "--output_filename", action="store", type="string", dest="outputfilename",
                  help="output tab delimited data file")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "queryfilename", "outputfilename"]
    
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    
    print "Reading in and formatting files..."
    inputfilename = options.inputfilename
    queryfilename = options.queryfilename
    outputfilename = options.outputfilename
    outputdirectory = outputfilename.rpartition('.')[0] + '.d'
    
    if not os.path.exists(outputdirectory):
        os.makedirs(outputdirectory)
    
    with open(inputfilename,'U') as infile:
        combined = pd.read_csv(infile, header=0, sep='\t')

    MTnames = combined.columns.tolist()[6:]
    annotnames = ["header", "bin_num", "function", "ontology", "organism", "taxonomy"]
    combined.columns = annotnames + MTnames

    
    #bin_list = list(combined.bin_num.unique())
    #bin_list.sort()
    zsum = zip(*[combined.bin_num.groupby(combined.bin_num).count().index, combined.bin_num.groupby(combined.bin_num).count().tolist()])
    zsum.sort(key=lambda x: x[0])
    bin_list = [bin for (bin, count) in zsum if count > 10]    
    
    combined.loc[:,'searchcol'] = combined.function.fillna('') +';' + combined.ontology.fillna('')
    combined.loc[:,'EC'] = combined.searchcol.str.extract('\([ ]{0,1}?EC[: ](\d+\.\d+\.\d+\.\d+)[ ]{0,1}?\)')
    comb = combined.searchcol.str.extract('(\w*) [Cc]hain|(\w*) [Ss]ubunit') + ';' + combined.searchcol.str.extract('[Cc]hain (\w*)|[Ss]ubunit (\w*)')
    combined.loc[:,'chain_or_subunit'] = comb.fillna('').sum(axis=1)
    
    with open(queryfilename, 'U') as queryfile:
        #qreader = csv.reader(queryfile, dialect='excel-tab')
        #queries = [for queryline in qreader]
        queries = pd.read_csv(queryfile, header=0, sep='\t')
    queries.columns = ["abbreviation", "qname", "chain_or_subunit", "code", "subunit", "EC", "exclude", "nested"]
    queries.chain_or_subunit = queries.chain_or_subunit.replace(';','|',regex=True)
    #queries.EC = queries.EC.replace(';','|',regex=True)
    queries.EC = queries.EC.replace('\.','\\\.',regex=True)
    #queries.qname = queries.qname.replace(';','|',regex=True)
    #queries.exclude = queries.exclude.replace(';','|',regex=True)
    querynames = queries.abbreviation.tolist()
                            
    print "Searching for functional genes..."    
    
    for qdex in queries.index:
        # 0 abbreviation
        # 1 name
        # 2 chain or subunit
        # 3 code
        # 4 subunit
        # 5 EC
        # 6 exclude
        # 7 nested  
        query = queries.iloc[qdex,:]  
        queryab = query.abbreviation
        combined.loc[:,queryab] = np.nan
        #searching_df = combined[query.abbreviation]
        if query.notnull().EC:
            combined.loc[combined.EC.notnull(), queryab] = False
            ecmaybe = combined.loc[combined.EC.str.contains(query.EC) == True]
            if query.notnull().chain_or_subunit or query.notnull().subunit:

                if query.notnull().chain_or_subunit:                
                    ecTF = pd.DataFrame(ecmaybe.chain_or_subunit.str.contains(query.chain_or_subunit))                
                if query.notnull().subunit:
                    queryprot = '\b' + query.code + '[' + query.subunit + ']\b'
                    if query.isnull().chain_or_subunit:                
                        ecTF = pd.DataFrame(ecmaybe.searchcol.str.contains(queryprot))
                    else:
                        ecTF = ecTF.join(pd.DataFrame(ecmaybe.searchcol.str.contains(queryprot))).any(axis=1)
                combined.loc[ecTF.index, queryab] = ecTF
            else:
                combined.loc[ecmaybe.index, queryab] = True
        if query.notnull().code:
            if query.isnull().subunit:
                querycode = '\b[' + query.code[0] + query.code[0].upper() + ']' + query.code[1:] + '\b'                
                codesearch_df = combined.loc[combined[queryab].isnull(),'searchcol'].str.contains(querycode)
                codesearch_df = codesearch_df[codesearch_df == True]
                combined.loc[codesearch_df.index, queryab] = True
            else:
                queryprot = '\b[' + query.code[0] + query.code[0].upper() + ']' + query.code[1:] + '[' + query.subunit + ']\b'
                codesearch_df = combined.loc[combined[queryab].isnull(),'searchcol'].str.contains(queryprot)
                codesearch_df = codesearch_df[codesearch_df == True]
                combined.loc[codesearch_df.index, queryab] = True		
        if query.notnull().qname:
            namesearch_df = combined.loc[combined[queryab].isnull()]
            combined.loc[namesearch_df.index, queryab] = False
            queryname = '(?i)' + query.qname
            namematch = namesearch_df[namesearch_df.searchcol.str.contains(queryname).fillna(False)]
            if query.notnull().chain_or_subunit:
                namematch = namematch[namematch.chain_or_subunit.str.contains(query.chain_or_subunit)]
            combined.loc[namematch.index, queryab] = True
                                
            if query.notnull().nested:
                for nquery in query.nested.split('|'):
                    nqueryabbr = queryab + '_' + nquery
                    querynames.append(nqueryabbr)
                    mnquery = nquery.replace(';','|')
                    allmatches = namematch.searchcol.str.contains(mnquery)
                    if isinstance(allmatches, pd.DataFrame):
                        nallmatches = allmatches.any(axis=1)
                    
                    combined.loc[:,nqueryabbr] = combined[queryab]
                    combined.loc[allmatches.index, nqueryabbr] = allmatches
                    combined.loc[allmatches[allmatches == True].index, queryab] = False
                                
        if query.notnull().exclude:
            combined.loc[combined.searchcol.str.contains(query.exclude).fillna(False), queryab] = False
                                                        
#   1. If EC code field is there, set fields with EC as False.  
#         If no EC field, skip step.
#         If EC match found, Set 'maybe'.  
#         If 'maybe', check if query chain or subunit exists.
#            If either query chain or field exists, search for chain or field match.  
#            If either field matches, set True
#         If no query field exists, set 'maybe' to True

#   2. If 3 digit code field is there, check for matches of the remaining:
#         If there is no subunit, check only for code
#            If code matches, set True
#         If subunit field exists, check for subunit and code match
#            If subunit and code matches, set True

#   3. If name field is there, check for name matches of the remaining:
#         Set all remainder to False
#         If name whole word matches, check if chain exists.
#            If chain field matches, set True.
#            If chain field mismatch, set False
#         If no chain field exists, set True
#         If nested field is there, 
#             for each nested item, 
#                 search for named hits and set True if matched
#                 set original field to false for all matches
#                 create a new abbreviation code and field from these
                                                 
#   4. If anything in exclude column matches in search column, set False
        
    print "Computing stats and writing..."

    with open(outputfilename, 'w') as outfile:
        writer = csv.writer(outfile, dialect='excel-tab')
        writer.writerow(["bin", 'log 2 median'] + querynames + ['score'] + querynames + ['counts'] + querynames)
        for bin in bin_list:
            binquery = str(bin).replace('.','\.')
            working_df = combined.loc[combined.bin_num.apply(str).str.contains(binquery), MTnames]
            abbrs_df = combined.loc[combined.bin_num.apply(str).str.contains(binquery), querynames]            
            log_df = np.log(working_df.applymap(float) / working_df.median())
            
            bin_abbr_stats = []
            gene_nums = []
            gene_counts = []
            for abbr in querynames:                   
                abbr_df = log_df.loc[abbrs_df[abbr] == True]
                gene_med = abbr_df.mean()
                gene_med = gene_med[gene_med != 0].median()
                bin_abbr_stats.append(gene_med)
                if np.isnan(gene_med) or np.isinf(gene_med):
                    gene_num = 0
                elif gene_med < -1:
                    gene_num = 1
                elif gene_med <= 1:
                    gene_num = 2
                elif gene_med > 1:
                    gene_num = 3
                gene_nums.append(gene_num)                    
                gene_counts.append(len(abbr_df.index))
                bin_org_df = combined.loc[combined.bin_num == bin, 'organism'].dropna().value_counts()
                if len(bin_org_df) > 0:
                    bin_org = str(bin_org_df.index[0])
                else:
                    bin_org = ''
            writer.writerow([bin, bin_org] + bin_abbr_stats + [''] + gene_nums + [''] + gene_counts)     
    
    for abbr in querynames:
        with open(outputdirectory + '/' + abbr + '.search_results.txt', 'w') as abbrfile:
            combined.loc[combined[abbr] == True, annotnames].to_csv(abbrfile, sep="\t", header=True, index=False)
            
    print "Done!"
