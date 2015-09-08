#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
Jackson Lee 11/20/14
This script reads in a tab delimited file of mg-rast sims with md5 keys and extracts the (first) top
md5 hit for each scaffold based on the e-value and outputs a tab delimited table

Input file format:
Query hitid %Id aligment_len mismatches gaps q.start q.end s.start s.end e_val bitscore


scaffold-0_5_1_231_+	0a8925a10b282925d82da645673f0089	74.29	35	37	44	78	7.6e-07	52.0
scaffold-0_5_1_231_+	f2642cd05d2188865c60c70187e6956f	74.29	35	37	44	78	5.8e-07	52.0
scaffold-0_5_1_231_+	4e7280d7a35f7d211224084187aebbe5	81.25	32	35	45	76	3.9e-06	49.0
scaffold-0_5_1_231_+	386485e1b6e09f7c04958288d74002c7	80.00	30	35	47	76	4.4e-05	46.0
scaffold-0_5_1_231_+	49441045aa390204c1e9503888a7bb62	80.00	30	35	47	76	4.4e-05	46.0
scaffold-0_5_1_231_+	458e9cf456892f31ae86f07510019a7e	62.86	35	13	0	3	37	43	77	1.7e-04	44.0
...
note some entries missing the mismatches, gaps, and q.start

Output file format:
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

   usage:
   pick_top_mgraast_sims_md5.py -i mgrast_organism.txt -e e_threshold -o output.file

---------------------------------------------------------------------------------------"""


#---------------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from optparse import OptionParser
from operator import itemgetter


#---------------------------------------------------------------------------------------

#function declarations


#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    pick_top_mgraast_sims_md5.py -i mgrast_organism.txt -e e_threshold -o output.file",                  
    description='Jackson Lee 11/20/14.  This script reads in a tab delimited file of mg-rast sims \
    with md5 keys and extracts the (first) top md5 hit for each scaffold based on the e-value \
    and outputs a tab delimited table.')    
    parser.add_option("-i", "--input_file", action="store", type="string", dest="inputfilename",
                  help="tab-delimited MGRAST sims file")
    parser.add_option("-e", "--e_value", action="store", type="float", dest="ethreshold", default=1.0,
                  help="maximum e-value cutoff (e.g. 1e-10)")
    parser.add_option("-o", "--output_filename", action="store", type="string", dest="outputfilename",
                  help="tab-delimited output file")
    (options, args) = parser.parse_args()

    mandatories = ["outputfilename","inputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    
    inputfilename = options.inputfilename    
    outputfilename = options.outputfilename  
    eval_threshold = float(options.ethreshold)
    print "Filtering on eval: " + str(eval_threshold)
        
    print "Read in sims file..."
    
    #get unique list of scaffolds
    infile_list = []
    scaffold_names = []
    with open(inputfilename,'U') as infile:
        for line in infile:
            scaffold_names.append("_".join(line.strip().split('\t')[0].split('_')[0:2]))            
    unique_queries = set(scaffold_names)
    
    scaffold_dict = {}
    for entry in list(unique_queries):
       scaffold_dict[entry] = ['', eval_threshold + 1.0]
    
    print "Processing sims file..."
    
    with open(inputfilename,'U') as infile:
        for line in infile:
            query_list = line.strip().split('\t')
            scaffold_name = "_".join(query_list[0].split('_')[0:2])
            #bit_score = float(query_list[-1])
            e_val = float(query_list[-2])
            md5 = query_list[1]
            if scaffold_dict[scaffold_name][1] > e_val:
                scaffold_dict[scaffold_name] = [md5, e_val] 
    
    print "Sorting and writing..."            
    with  open(outputfilename,'w') as outfile:           
        for (name, tuple) in sorted(scaffold_dict.items(), key=itemgetter(0)):
            if tuple[1] <= eval_threshold:
                outfile.write(name + '\t' +tuple[0] + '\n')
        
    print "Done!"
