#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
Jackson Lee 11/11/14
This script reads in a tab delimited file of mg-rast organism annotations with md5 keys
and determines a unique search set to lookup in the mgrast md5 tab delimited database file.
The script then searches the database and outputs a tab delimited taxonomic lineage file.

Input file format:
scaffold-384330_1	00000d5aae0fe4dbc5bb1fa19a11f2d7
scaffold-362293_1	00001a0a5381c6474e16caef49875320
scaffold-61728_6	00001a0a5381c6474e16caef49875320
scaffold-18247_1	000025d4fcb8dfe23b1025d6ce3fbc3d
scaffold-6823_3	000025d4fcb8dfe23b1025d6ce3fbc3d
scaffold-130286_1	0000262e4f74782ab3e1f18e68690812
scaffold-392084_1	0000a0c3ed326a21b2da95799f1641a8
scaffold-377521_1	0000ab57cc5e20095a0a8d162b35b3cc
scaffold-222332_1	0001032daa1eea5a5c470dd2fa1de8c3
...

Taxonomy database format:
0000029042cc6c69f2b830142508acb1	Bacteria	unclassified (derived from Bacteria)	unclassified (derived from Bacteria)	unclassified (derived from Bacteria)	unclassified (derived from Bacteria)	unclassified (derived from Bacteria)	uncultured bacterium	uncultured bacterium	8
000002aa15832b94a71e3c7de643c267	Bacteria	Synergistetes	Synergistia	Synergistales	Synergistaceae	Pyramidobacter	Pyramidobacter piscolenPyramidobacter piscolens W5455	8
000002e3b0d3f405d984bd1ee95d7fd1	Bacteria	Proteobacteria	Gammaproteobacteria	Xanthomonadales	Xanthomonadaceae	Xanthomonas	Xanthomonas gardneri	Xanthomonas gardneri ATCC 19865	8
...

Output file format:
A tab delimited file of 
contig-faa-name\tlineage
scaffold-384330_1	Bacteria;unclassified (derived from Bacteria);unclassified (derived from Bacteria);unclassified (derived from Bacteria)	unclassified (derived from Bacteria);unclassified (derived from Bacteria);uncultured bacterium	uncultured bacterium
scaffold-362293_1	Eukaryota;Chordata;Aves;Passeriformes;Muscicapidae;Ficedula;Ficedula albicollis;Ficedula albicollis
...

   usage:
   query_mgrast_md5_taxonomy.py -i mgrast_organism.txt -t md5_lca_map.tab -o output.file
"""
#---------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from optparse import OptionParser

#---------------------------------------------------------------------------------------

#function declarations


#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    query_mgrast_md5_taxonomy.py -i mgrast_organism.txt -t md5_lca_map.tab -o output.file",                  
    description='Jackson Lee 11/11/14.  This script reads in a tab delimited file of mg-rast organism annotations with md5 keys \
and determines a unique search set to lookup in the mgrast md5 tab delimited database file. \
The script then searches the database and outputs a tab delimited taxonomic lineage file.')    
    parser.add_option("-i", "--input_file", action="store", type="string", dest="inputfilename",
                  help="tab-delimited MGRAST organism annotation file")
    parser.add_option("-t", "--md5_lca_file", action="store", type="string", dest="taxfilename",
                  help="tab-delimited MGRAST md5 lca file")                  
    parser.add_option("-o", "--output_filename", action="store", type="string", dest="outputfilename",
                  help="tab-delimited output file")
    (options, args) = parser.parse_args()

    mandatories = ["outputfilename","inputfilename","taxfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    
   
    inputfilename = options.inputfilename    
    taxfilename = options.taxfilename     
    outputfilename = options.outputfilename  
        
    print "Read in annotations file..."
    infile_list = []
    unique_queries = []
    with open(inputfilename,'U') as infile:
        for line in infile:
            query_list = line.strip().split('\t')
            infile_list.append(query_list)            
    unique_queries = set([md5hash[1] for md5hash in infile_list])
    
    print "Extracting " + str(len(unique_queries)) + " unique annotations from database..."
    tax_dict = {}
    with open(taxfilename, 'U') as taxfile:
        for line in taxfile:
            tax_list = line.strip().split('\t')
            if tax_list[0] in unique_queries:
                tax_string = ';'.join(map(str,tax_list[1:-1]))
                tax_dict[tax_list[0]] = tax_string
                if len(tax_dict) % 10000 == 0:
                    print str(len(tax_dict)) + ' entries extracted...'
        
    print "Matching taxonomies and writing..."            
    with  open(outputfilename,'w') as outfile:           
        for entry in infile_list:
            if entry[1] in tax_dict:
                outfile.write(entry[0] + '\t' + tax_dict[entry[1]] + '\n')
            else:
                outfile.write(entry[0] + '\tNone\n')
        
    print "Done!"
