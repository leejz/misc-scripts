#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
Jackson Lee 11/20/14
This script reads in a tab delimited file of sequence headers with md5 keys
and determines a unique search set to lookup in the mgrast md5 tab delimited database file.
The script then searches the database and outputs a tab delimited annotations file for protein/rna,
ontology, and organism for each protein sequence.  Note that all databases must be in the same directory
and conform to the original MG-RAST naming format (md5_lca_map, etc.).  Now with cluster file support!

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

Cluster file format:
scaffold-640020_1_1_10506_+	scaffold-10209_1_1_7317_+,scaffold-515549_1_1_1932_+	99.38%,96.73%
scaffold-55003_8_1_9660_+	scaffold-1843_1_1_8334_+,scaffold-137647_2_1_9660_+	99.68%,99.91%
scaffold-609926_2_1_9537_+	scaffold-63671_1_1_7563_+	99.92%
scaffold-18344_12_1_9345_+	scaffold-463682_3_1_9345_+	99.84%

singletons not listed in the cluster file

Annotation database formats:

==> ontology_map <==
format: ontology_id	name	ontology_system_id

70832	NOG87308	13
70890	NOG87469	13
28533	NOG05383	13
28534	NOG05390	13
28535	NOG05398	13
28536	NOG05400	13
28537	NOG05420	13
28538	NOG05431	13
28539	NOG05437	13
28540	NOG05444	13
...

==> function_map <==
format: function_id	name

1	..
2	000C10C11
3	000C19H04
4	0.0.1
5	001R
6	002 mRNA peptide
7	002R
8	003 mRNA peptide
9	003R
10	004R
...

==> organism_map <==
format: organism_id	organism_name

2	44AHJD-like phages Staphylococcus phage SAP-2	
31	Abaeis niccipe (Sleepy orange) (Eurema nicippe)	
75	Abelia grandiflora (Glossy abelia) (Abelia chinensis x Abelia uniflora)
206	Abramis sapa (white-eye bream)	
193	Abralia sp	
250	Abronia sp	
305	Abrus precatorius, Peptide, 267 aa	
306	Abrus precatorius, seeds, Peptide, 268 aa	
364	Aburria pipile (Common piping guan) (Trinidad piping guan)	
374	Abutilon mosaic virus (isolate West India) (AbMV)...
...

==> md5_ontology_map <==
format: md5	ontology_source_id	function_id	ontology_id

000006c1c3a2689dd37477e976a239a1	13	277543	35147
00000d86d1985d7a0330e84b3710d671	14	613619	72268
00001508eba3f78863a4f9cb2463810d	10	4590510	23978
00001508eba3f78863a4f9cb2463810d	12	5792349	439
00001508eba3f78863a4f9cb2463810d	14	5535576	77176
0000178803490f6a09275722107983b4	14	4507452	17691
0000178803490f6a09275722107983b4	14	4507688	17693
0000190b67bc6d32bbf31de11136ae14	14	4507195	74912
00001a757949ba4df5f1a9f8f6ba6c09	12	5786841	1212
00001aba8aee0c90a80969ea8da059f8	12	5574599	2574
...

==> md5_protein_map & md5_rna_map <==
format: md5	protein_source_id	function_id	organism_id

00000083b5cacb61de38fc94dffce1b9	6	5134591	501475
00000083b5cacb61de38fc94dffce1b9	2	5134591	501475
00000083b5cacb61de38fc94dffce1b9	21	5134591	501475
000001961cb2de9aa0eea4a05eaa8843	3	8243072	503157
000001a9cbb2d314d4c5c7fa64fd5dde	6	1229839	529285
000001a9cbb2d314d4c5c7fa64fd5dde	2	1229839	529285
000001a9cbb2d314d4c5c7fa64fd5dde	21	1229840	529285
000001c58edf6adc620804295e1a0e2c	2	2834566	260427
000001c58edf6adc620804295e1a0e2c	21	4893953	470556
0000020f99fd2a3b134589288b97f730	5	248460	596808
...

note: multiple md5 entries exist for each source type

Output file format:

Ontology:
A tab delimited file of format:
contig-faa-name	ontology_term	annotation
scaffold-384330_1	NOG05383|ontology annotation 1;NOG05385|additional onotologies; etc.
scaffold-362293_1	NOG05384|ontology annotation 2
...

Protein / RNA:
contig-faa-name	annotation
scaffold-384330_1	function 1; additional functions; etc.
scaffold-362293_1	function 2
...

   usage:
   query_mgrast_md5_annotation.py -i top.md5.txt -c aa90.cluster.file -e e_val_threshold -d md5_database_directory -o output.prefix -s 1,2,3
"""
#---------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from optparse import OptionParser
from csv import reader, writer
from operator import itemgetter
import time

#---------------------------------------------------------------------------------------

#function declarations


#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    query_mgrast_md5_annotation.py -i top.md5.txt -c aa90.cluster.file -e e_val_threshold -d md5_database_directory -o output.prefix -s 1,2,3",                  
    description='Jackson Lee 11/20/14.  This script reads in a tab delimited file of sequence headers with md5 keys \
and determines a unique search set to lookup in the mgrast md5 tab delimited database file. \
The script then searches the database and outputs a tab delimited annotations file for protein/rna, \
ontology, and organism for each protein sequence.  Note that all databases must be in the same directory \
and conform to the original MG-RAST naming format (md5_lca_map, etc.) Now with cluster file support!')    
    parser.add_option("-i", "--input_file", action="store", type="string", dest="inputfilename",
                  help="tab-delimited MGRAST 650 Sims file")
    parser.add_option("-c", "--cluster_file", action="store", type="string", dest="clusterfilename",
                  help="tab-delimited MGRAST 550 aa90 cluster file")
    parser.add_option("-d", "--md5_database_directory", action="store", type="string", dest="dbdir",
                  help="tab-delimited MGRAST md5 lca file")                  
    parser.add_option("-o", "--output_filename", action="store", type="string", dest="outputfilename",
                  help="tab-delimited output file")
    parser.add_option("-e", "--e_value", action="store", type="float", dest="ethreshold", default=1.0,
                  help="maximum e-value cutoff (e.g. 1e-10)")              
    parser.add_option("-t", "--cutoff_id", action="store", type="float", dest="cutoff", default=1.0,
                  help="minimum id cutoff % (e.g. 50)")
    parser.add_option("-s", "--source_filters", action="store", type="string", dest="sources", default="all",
                  help="comma-delimited list of source type restrictions, prioritized first e.g. 11,12,13, use \"view\" to see list")                  
    (options, args) = parser.parse_args()

    mandatories = ["dbdir"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
   
    if options.dbdir[-1] == "/":
        dbdir = options.dbdir     
    else:
        dbdir = options.dbdir + "/"

    all_sources = range(2,25)
    if options.sources == "view":
        with open(dbdir + "source_map", 'U') as sourcefile:
            print "Opening source_map\n"
            for line in sourcefile:
                print line.strip()
        exit(-1)
    elif options.sources != "all":
        sourcelist = map(int,options.sources.strip().split(','))
        for sourcenum in sourcelist:
            if sourcenum not in all_sources:
                print "Source number not int list of sources, exiting..."
                exit(-1)            
    else:
        sourcelist = all_sources

    mandatories = ["outputfilename","inputfilename", "clusterfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
            
    inputfilename = options.inputfilename    
    outputfilename = options.outputfilename  
    clusterfilename = options.clusterfilename
        
    md5_db_list = ["md5_protein_map", "md5_rna_map"]
    md5_ontology = "md5_ontology_map"
        
    print "Read in MGRAST files and database files..."
    #read in infile completely, and read in function_map and ontology_map as dictionaries
    infile_list = []
    unique_queries = []
    with open(inputfilename,'U') as infile:
        inreader = reader(infile, dialect='excel-tab')
        for query_list in inreader:
            #faaname = "_".join(query_list[0].split('_')[0:2])
            faaname = query_list[0]
            e_val = float(query_list[-2])
            cutoff = float(query_list[2])
            md5 = query_list[1]            
            infile_list.append([faaname, md5, cutoff, e_val])            
            unique_queries.append(md5)
    unique_queries = set(unique_queries)
    
    with open(clusterfilename, 'U') as clusterfile:
        clustreader = reader(clusterfile, dialect='excel-tab')
        clust_dict = {}
        for clustlist in clustreader:
            clust_name = clustlist[0]
            clust_members = clustlist[1].split(',')
            clust_confidence = clustlist[2] # not yet implemented
            if clust_name not in clust_dict:
                clust_dict[clust_name] = clust_members                

    # read each definition db and store as dict
    ref_func_dict = {}
    with open(dbdir + "function_map", 'U') as functionfile:
        funcreader = reader(functionfile, dialect='excel-tab')
        for funclist in funcreader:
            ref_func_dict[funclist[0]] = funclist[1]
                
    ref_ont_dict = {}
    with open(dbdir + "ontology_map", 'U') as ontfile:
        ontreader = reader(ontfile, dialect='excel-tab')
        for ontlist in ontreader:
            ref_ont_dict[ontlist[0]] = ontlist[1]
                
    ann_dict = {}
    print "Extracting " + str(len(unique_queries)) + " unique annotations from protein & rna database..."   
    # for each md5 database, match unique md5s to each respective database entry and get the function from function dictionary
    for md5filename in md5_db_list:
        with open(dbdir + md5filename, 'U') as md5file:
            print "Extracting " + md5filename
            annreader = reader(md5file, dialect='excel-tab')
            for ann_list in annreader:
                md5 = ann_list[0]
                sourcenum = int(ann_list[1])
                funcstr = ann_list[2]
                if md5 in unique_queries and sourcenum in sourcelist:
                    if md5 in ann_dict:
                        if funcstr != '':
                            ann_dict[md5].append([sourcelist.index(sourcenum),ref_func_dict[funcstr]])
                    else:
                        if funcstr != '':
                            ann_dict[md5] = [[sourcelist.index(sourcenum),ref_func_dict[funcstr]]]
                        if len(ann_dict) % 10000 == 0:
                            print str(len(ann_dict)) + ' entries extracted...'
    print str(len(ann_dict)) + ' entries extracted...'    
    time.sleep(5)
    
    ont_dict = {}
    with open(dbdir + md5_ontology, 'U') as md5file:
        print "Extracting " + str(len(unique_queries)) + " unique annotations from " + md5_ontology + " database..."
        #for the md5 ontology db, match unique md5s and get the ontology function and number from the ontology dictionary
        annreader = reader(md5file, dialect='excel-tab')
        for ann_list in annreader:
            md5 = ann_list[0]
            sourcenum = int(ann_list[1])
            funcstr = ann_list[2]
            ontstr = ann_list[3]
            if md5 in unique_queries and sourcenum in sourcelist:
                if md5 in ont_dict:
                    if funcstr != '' and ontstr != '':            
                        ont_dict[md5].append([sourcelist.index(sourcenum), str(ref_func_dict[funcstr])+ '|' + str(ref_ont_dict[ontstr])])
                else:
                    if funcstr != '' and ontstr != '':            
                        ont_dict[md5] = [[sourcelist.index(sourcenum), str(ref_func_dict[funcstr])+ '|' + str(ref_ont_dict[ontstr])]]
                    if len(ont_dict) % 10000 == 0:
                        print str(len(ont_dict)) + ' entries extracted...'
    
    print str(len(ont_dict)) + ' entries extracted...'    
    print "Matching md5s and writing..." 
    
    eval_threshold = float(options.ethreshold)
    cutoff_threshold = float(options.cutoff)
    print "Filtering on e-value: " + str(eval_threshold)
    print "Filtering on cutoff < " + str(cutoff_threshold)
               
    faa_anndict = {}
    faa_ontdict = {}
        
    #for each line in the sims file retain the best hit from duplicate headers, and keep the best entries from each annotation set
    #then order annotations by source list order and output in semi-colon delimiters
    for entry in infile_list:
        faaname = entry[0]
        e_val = float(entry[-1])
        cutoff = float(entry[-2])
        md5 = entry[1]
        
        if md5 in ann_dict:
            annotlist = [annot[1] for annot in sorted(ann_dict[md5], key=itemgetter(0))]
            annotstr = ';'.join(map(str,annotlist))
            if faaname not in faa_anndict:
                faa_anndict[faaname] = [cutoff, e_val, annotstr]
            elif faa_anndict[faaname][1] > e_val:            
                faa_anndict[faaname] = [cutoff, e_val, annotstr]

        if md5 in ont_dict:
            annotlist = [annot[1] for annot in sorted(ont_dict[md5], key=itemgetter(0))]
            annotstr = ';'.join(map(str,annotlist))
            if faaname not in faa_ontdict:
                faa_ontdict[faaname] = [cutoff, e_val, annotstr]
            elif faa_ontdict[faaname][1] > e_val:            
                faa_ontdict[faaname] = [cutoff, e_val, annotstr]

    #write each best match for each file if it passes the e-value threshold
    with  open(outputfilename + ".protein_rna.annotations.txt" ,'w') as outfile:           
        annwriter = writer(outfile, dialect='excel-tab')
        for (name, tuple) in sorted(faa_anndict.items(), key=itemgetter(0)):
            if tuple[1] <= eval_threshold and tuple[0] > cutoff_threshold:
                if name in clust_dict:
                    cluster_names = [name] + clust_dict[name]
                else:
                    cluster_names = [name]
                for cluster_mem in cluster_names:
                    annwriter.writerow(["_".join(cluster_mem.split('_')[0:2]), tuple[2] + "; %ID=" + str(tuple[0])])                

    with  open(outputfilename + ".ontology.annotations.txt" ,'w') as outfile:   
        ontwriter = writer(outfile, dialect='excel-tab')
        for (name, tuple) in sorted(faa_ontdict.items(), key=itemgetter(0)):        
            if tuple[1] <= eval_threshold and tuple[0] > cutoff_threshold:
                if name in clust_dict:
                    cluster_names = [name] + clust_dict[name]
                else:
                    cluster_names = [name]
                for cluster_mem in cluster_names:
                    ontwriter.writerow(["_".join(cluster_mem.split('_')[0:2]), tuple[2] + "; %ID=" + str(tuple[0])])                

        
    print "Done!"
