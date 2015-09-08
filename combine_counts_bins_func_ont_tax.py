#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
Jackson Lee 11/21/14
This script reads in a counts, phylogeny, bin, function, ontology and taxonomy tab-delimited files 
   and combines identical header records in a tab delimited format.  This script will take
   counts from each sample and normalize all genes to the sample average per base RPKM.  This combined
   data is written as a tab-delimited file for each unique sequence file header.
   
   Then the script sums duplicate ontology-organism RPKM coverages and consolidates the records, 
   sorts by bin then ontology, and writes an excel tab delimited file with RPKMs for 
   each sample.
   
   Input file formats:
   Counts:
   header   bplength   avg. per base depth   avg. per base depth   avg. per base depth   etc.
   scaffold-0 2552	102.1	105.3	0.0	4.0 etc.
   ...
   one line for each record, header serves as index
   
   Input bin format:
   scaffold-0	1
   scaffold-1	1
   ...
   not all sequences have records
      
   Input function format:
   scaffold-0_10	InsA-like protein
   scaffold-0_12	30S ribosomal protein S4
   scaffold-0_13	Molybdenum cofactor synthesis-like protein
   ...
   not all sequences have records, multiple records separated by ';'
   
   Input ontology format:
   scaffold-0_42	glutathione S-transferase [EC:2.5.1.18]|K00799
   scaffold-10005_4	UDP-glucose 4-epimerase [EC:5.1.3.2]|K01784
   scaffold-100084_1	tryptophan synthase alpha chain [EC:4.2.1.20]|K01695
   scaffold-1000_14	phenylacetate-CoA ligase [EC:6.2.1.30]|K01912
   ...
   not all sequences have records, multiple records separated by ';'
   note: EC numbers don't exist for all records

   Input phylogeny format:
   scaffold-0_14	Bacteria;Cyanobacteria;unclassified (derived from Cyanobacteria);Oscillatoriales;unclassified (derived from Oscillatoriales);Coleofasciculus;Coleofasciculus chthonoplastes;Coleofasciculus chthonoplastes PCC 7420
   scaffold-0_16	Bacteria;Cyanobacteria;unclassified (derived from Cyanobacteria);Oscillatoriales;unclassified (derived from Oscillatoriales);Lyngbya;Lyngbya sp. PCC 8106;Lyngbya sp. PCC 8106
   ...
   not all sequences have records

      
   Output file format:
   database format:
   header	bin_num	function	ontology	organism	taxonomy	Sample_name_RPKM	etc.
   scaffold-0_42	1	InsA-like protein	glutathione S-transferase [EC:2.5.1.18]|K00799	Lyngbya sp. PCC 8106	Bacteria;Cyanobacteria;unclassified (derived from Cyanobacteria);Oscillatoriales;unclassified (derived from Oscillatoriales);Lyngbya;Lyngbya sp. PCC 8106;Lyngbya sp. PCC 8106	105.2
   ...
   
   summary.ontology format:
   bin	organism	ontology	Sample_name_RPKM etc.
   1	Lyngbya sp. PCC 8106	K00799	105.2  etc.
   1	Lyngbya sp. PCC 8106	protein_where_avail	105.2  etc.
   no_bin	no_organism_scaffold-0_21	no_ontology_scaffold-0_21	100021.2	etc.
   ...
   
   usage:
   combine_counts_bins_func_ont_tax.py -c counts.txt -b bins.txt -f function.txt -y ontology.txt -t taxa.txt -o out.prefix

---------------------------------------------------------------------------------------"""
#Header - Linkers, Libs, Constants
from string import strip
from optparse import OptionParser
import csv

#function declarations

#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: combine_counts_bins_func_ont_tax.py -c counts.txt -b bins.txt -f function.txt -y ontology.txt -t taxa.txt -o out.prefix",                  
    description="JZL 11/21/14 This script reads in a counts, phylogeny, bin, function, ontology and taxonomy tab-delimited files  \
and combines identical header records in a tab delimited format.  This script will take \
counts from each sample and normalize all genes to the sample average per base RPKM.  This combined \
data is written as a tab-delimited file for each unique sequence file header. \
Then the script sums duplicate ontology-organism RPKM coverages and consolidates the records, \
sorts by bin then ontology, and writes an excel tab delimited file with RPKMs for \
each sample.")
    parser.add_option("-c", "--counts_file", action="store", type="string", dest="coveragefilename",
                  help="tab delimited index file of all count libraries")
    parser.add_option("-b", "--bin_file", action="store", type="string", dest="binfilename",
                  help="tab delimited bin file")
    parser.add_option("-f", "--function_file", action="store", type="string", dest="functionfilename",
                  help="tab delimited protein function file")
    parser.add_option("-y", "--ontology_file", action="store", type="string", dest="ontologyfilename",
                  help="tab delimited ontology file (See DocString for format)")
    parser.add_option("-t", "--taxonomy_file", action="store", type="string", dest="taxonomyfilename",
                  help="tab delimited taxonomy file")
    parser.add_option("-o", "--output_prefix", action="store", type="string", dest="outputfilename",
                  help="prefix for output tab delimited record files")
    (options, args) = parser.parse_args()

    mandatories = ["coveragefilename", "binfilename", "functionfilename", "ontologyfilename", "taxonomyfilename", "outputfilename"]
    
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
            
    filenames = [options.coveragefilename, options.binfilename, options.functionfilename, options.ontologyfilename, options.taxonomyfilename, options.outputfilename]
            
    #read in coverage file, the most complete record, and get index and totals information
    print "Processing counts and index..."
    with open(filenames[0], 'U') as coveragefile:
        reader = csv.reader(coveragefile, dialect='excel-tab')
        coverage_data =[]
        firstline = reader.next()
        sample_names = firstline[2:]
        total_coverage = [0.0] * len(sample_names)        
        for line in reader:
            coverage_data.append(line)
            total_coverage = [int(line[1])*count + sumcov for count, sumcov in zip(map(float,line[2:]), total_coverage)]

    tot_cov_M = [totcov/1000000/1000 for totcov in total_coverage]
    
    print "Reading annotation records..."      
    #read in each annotation file and store as a dictionary
    
    annotations_list = []
    for i, annotationfilename in enumerate(filenames[1:5]):
        annotations_list.append({})
        with open(annotationfilename, 'U') as annotationfile:
            reader = csv.reader(annotationfile, dialect='excel-tab')
            for entry in reader:
                if entry[0] not in annotations_list[i]:
                    annotations_list[i][entry[0]] = entry[1] 
                else:
                    annotations_list[i][entry[0]] = annotations_list[i][entry[0]] + ';' + entry[1]

    #if bin file is a orf gene annotation use that, else parse the contig name
    if '_' in ''.join(annotations_list[0].keys()):
        contigflag = False
    else:
        contigflag = True
    
    outputdatafilename = filenames[-1] + '.data.txt'
    outputsummaryfilename = filenames[-1] + '.summary.txt'
    
    print "Writing " + outputdatafilename
    output_list = []
    for line in coverage_data:
        faaname = line[0]
        bplen = line[1]
        coverages = [cov/tot_cov for cov, tot_cov in zip(map(float, line[2:]), tot_cov_M)]
                
        #if bin file is a orf gene annotation use that, else parse the contig name
        if contigflag:
            contigname = faaname.split('_')[0]
        else:
            contigname = faaname
                
        if contigname in annotations_list[0]:
            bin = annotations_list[0][contigname]
        else:
            bin = 'background'
        
        if faaname in annotations_list[1]:
            function = annotations_list[1][faaname]
        else:
            function = 'putative_protein_' + faaname
        
        if faaname in annotations_list[2]:
            ontology = annotations_list[2][faaname]
        else:
            ontology = ''
        
        if faaname in annotations_list[3]:
            tax = annotations_list[3][faaname]
            org = tax.split(';')[-1]
        else:
            tax = ''
            org = ''
        output_list.append([faaname, bin, function, ontology, org, tax] + coverages)
        
    #sort on bin and function, then write to file
    sorted_records = sorted(output_list, key=lambda x: (x[1], x[2]))
    with open(outputdatafilename, 'w') as outputdatafile:
        writer = csv.writer(outputdatafile, dialect='excel-tab')
        writer.writerow(['header', 'bin_num', 'function', 'ontology', 'organism', 'taxonomy'] + sample_names)
        for line in sorted_records:
            writer.writerow(line)
            
    print "Writing " + outputsummaryfilename    
    output_dict = {}
    for line in sorted_records:
        faaname = line[0]
        
        if line[3] == '':
            ontology = line[2]
        else:
            ontology = line[3].lower()

        if line[4] == '':
            org = 'no_taxa_in_' + faaname
        else:
            org = line[4]

        if line[1] == 'background':
            bin = 'putative_bin_from_' + org
        else:
            bin = line[1]
        
        coverages = map(float, line[6:])
        
        if (bin, ontology) in output_dict:
            output_dict[(bin, ontology)] = output_dict[(bin, ontology)][0:3] + [cov + dcov for cov, dcov in zip(coverages, output_dict[(bin, ontology)][3:])]
        else:
            output_dict[(bin, ontology)] = [bin, org, ontology] + coverages 
 
    #sort records on bin and ontology then write to file
    sorted_records = sorted(output_dict.values(), key=lambda x: (x[0], x[2]))
    with open(outputsummaryfilename, 'w') as outputdatafile:
        writer = csv.writer(outputdatafile, dialect='excel-tab')
        writer.writerow(['bin', 'organism', 'ontology'] + sample_names)
        for line in sorted_records:
            writer.writerow(line)
        
    print "Done!"
