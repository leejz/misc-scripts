#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 1/28/14

This script reads in a file and a tab delimited text file of [match]/t[replace] and
replaces all instances and reports back result and file.
   
Input fasta file format:
any fasta file
   
Input filter file format:
>Sequence0000000001    Seq1replaced
   
Output
fasta file with header replaced
a not found file with enteries not found written as 'outfile.notfound.*'
   
--------------------------------------------------------------------------------   
usage:   replace_from_file.py -i in.file -f filter.txt -o out.file
"""

#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = ArgumentParser(usage = "replace_from_file.py -i in.file -f filter.txt -o out.file",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_file", action="store", 
                        dest="inputfilename",
                        help="text input file")
    parser.add_argument("-f", "--filter_text", action="store", 
                        dest="filterfilename",
                        help="filter header file")
    parser.add_argument("-o", "--output_file", action="store", 
                        dest="outputfilename",
                        help="text output file")
    options = parser.parse_args()

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
    with open(filterfilename, 'U') as filterfile:
        filterfile_text =[]
        for line in filterfile:
            query, replace = line.strip().split('\t')
            filterfile_text.append([query, replace])
    
    with open(inputfilename,'U') as infile, open(outputfilename, 'w') as outfile, open(notfoundfilename, 'w') as notfoundfile:
        print "Replacing...."        
        for line in infile:
            new_file_text = ''
            #only search if header
            #if line[0] == '>':
            notfoundflag = True
            for [query, replace] in filterfile_text:    
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

    print "Done!"
