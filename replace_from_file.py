#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""Jackson Lee 1/28/14"""
"""This script reads in a file and a tab delimited text file of [match]/t[replace] and
   replaces all instances and reports back result and file.
   
   Input fasta file format:
   any fasta file
   
   Input filter file format:
   >Sequence0000000001    Seq1replaced
   
   Output
   fasta file with header replaced
   a not found file with enteries not found written as 'outfile.notfound.*'
   
   usage:
   replace_from_file.py -i in.file -f filter.txt -o out.file
"""

"""---------------------------------------------------------------------------------------"""
"""Header - Linkers, Libs, Constants"""
from string import strip
from optparse import OptionParser

"""function declarations"""

"""---------------------------------------------------------------------------------------"""
"""Body"""
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage:    replace_from_file.py -i in.file -f filter.txt -o out.file",                  
    description='7/16/13 replace_from_file.py This script reads in a file and a tab delimited text file of [match]/t[replace] and replaces all instances and reports back result and file.')
    parser.add_option("-i", "--input_file", action="store", type="string", dest="inputfilename",
                  help="text input file")
    parser.add_option("-f", "--filter_text", action="store", type="string", dest="filterfilename",
                  help="filter header file")
    parser.add_option("-o", "--output_file", action="store", type="string", dest="outputfilename",
                  help="text output file")
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "filterfilename", "outputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
            
    inputfilename = options.inputfilename
    filterfilename = options.filterfilename
    outputfilename = options.outputfilename
    outputfilenameprefix, dummy, extension = outputfilename.rpartition('.')
    notfoundfilename = outputfilenameprefix + '.notfound.txt'
    
    #read in filter file
    filterfile = open(filterfilename, 'U')
   
    filterfile_text =[]
    for line in filterfile:
        query, replace = line.strip().split('\t')
        filterfile_text.append([query, replace])
    filterfile.close()
    
    infile = open(inputfilename,'U')    
    outfile = open(outputfilename, 'w')
    notfoundfile = open(notfoundfilename, 'w')

    print "Replacing...."        
    for line in infile:
        new_file_text = []
        #only search if header
        #if line[0] == '>':
        notfoundflag = True
        for i, [query, replace] in enumerate(filterfile_text):    
            if query in line:
                new_file_text = line.replace(query, replace)
                notfoundflag = False
                #assuming only 1 match remove from search
                #filterfile_text.pop(i)          
                break      
        if notfoundflag:
            notfoundfile.write(line)  
            new_file_text = line    
        #else:
        #    new_file_text = line
	outfile.write(new_file_text)
    infile.close()
    outfile.close()
    notfoundfile.close()

    print "Done!"
