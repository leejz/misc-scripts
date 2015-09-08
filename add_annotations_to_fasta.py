#!/usr/bin/env python
"""---------------------------------------------------------------------------------------
Jackson Lee 1/28/14
This script reads in a fasta file and a tab delimited text file of annotations and
   replaces the header line with matched annotations
   
   Input fasta file format:
   any fasta file
   
   Input annotations file format:
   tab delimited headings of annotation names (1 word), with search string first column
   followed by tab delimited annotation data
   
   Output
   fasta file with header replaced
   a not found file with enteries not found written as 'outfile.notfound.*'
   
   usage:
   add_annotations_to_fasta.py -i in.fasta -a annotations.txt -o out.file


---------------------------------------------------------------------------------------"""
#Header - Linkers, Libs, Constants
from string import strip
from optparse import OptionParser
from Bio import SeqIO

#function declarations
def add_annot(records, notfoundfile):
    """this is a generator function to create the new record if needed"""    
    for record in records:
        if record.id in all_annotations:
            record.description = '\t'.join([header + '=[' + annotation + ']' for header, annotation in zip(all_headers, all_annotations[record.id])])
        else:
            notfoundfile.write(record.id + '\n')
            record.description = ''
        yield record

#---------------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: add_annotations_to_fasta.py -i in.fasta -a annotations.txt -o out.file",                  
    description='1/28/14 add_annotations_to_fasta.py, basic fasta file header query and add annotations')
    parser.add_option("-i", "--input_file", action="store", type="string", dest="inputfilename",
                  help="text fasta file")
    parser.add_option("-a", "--annotations_text", action="store", type="string", dest="annotationfilename",
                  help="tab-delimited annotations text file, first line headings, followed by entries for each sequence")
    parser.add_option("-o", "--output_file", action="store", type="string", dest="outputfilename",
                  help="fasta output file")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "annotationfilename", "outputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
            
    inputfilename = options.inputfilename
    annotationfilename = options.annotationfilename
    outputfilename = options.outputfilename
    outputfilenameprefix, dummy, extension = outputfilename.rpartition('.')
    notfoundfilename = outputfilenameprefix + '.notfound.txt' 
    
    print "Reading annotations..."
    with open(annotationfilename) as annotationfile:
        #build a list of annotation dictionaries
        all_annotations = {}
        all_headers = annotationfile.next().strip().split('\t')[1:]
        for line in annotationfile:
            linelist = line.strip().split('\t')
            key = linelist[0]
            value = linelist[1:]
            all_annotations[key] = value

    print "reading sequence files and adding annotations..."
    
    with open(inputfilename, 'U') as inputfile, open(outputfilename, 'w') as outputfile, \
open(notfoundfilename, 'w') as notfoundfile:
        input_seq_iterator = SeqIO.parse(inputfile, "fasta")
                 
        SeqIO.write(add_annot(input_seq_iterator, notfoundfile), outputfile, "fasta")
    
    print "Done!"
