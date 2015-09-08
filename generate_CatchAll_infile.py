#!/usr/bin/python
"""4/13/12 JZL
   This script reads a tab-delimited file containing abundance data and returns the correct formatted
   histogram files for each sample to run by CatchAll CatchAllCmdL.exe.
   
   usage:
   python generate_CatchAll_infile.py -i input_directory -o output_dir
   
   abundance otu table file format:
   a csv file with each environment in vertical columns, with the name of the environment first
   #rarefaction_750_4.txt
   #OTU ID	Ob.1	Ob.62Z
   103	0	0
   41	0	0
   30	0	0
   10	0	0
   9	0	0
   etc
   
   outfile format:
   a comma delimited file for each sample, where the first term is the frequency of counts, the 
   second is the number of OTUs at that count, sorted in the order of increasing counts
   CatchAll.Total.txt
   1,90
   2,12
   3,14
   4,1
   ...
   103,1
   etc
   
   CatchAll.Ob.1.txt
   ...
   
   The script generates a shell file 'CatchAll.sh' to run each sample as well

"""
"""------------------------------------------------------------------------------------------"""
"""Functions & Declarations"""

"""------------------------------------------------------------------------------------------"""
def generate_catchall_file(input_dir, filename, output_dir):
    """ def generate_catchall_file(input_dir, filename, output_dir):
    input_dir is the input directory full path 
    filename is the txt file to parse
    output_dir is the output directory full path
    
    return output_paths the list of filenames used with full path
    
    This function parses an OTU table for use in Catchall input format
    """
    # read in first line as sample names, then read in all data
    infile = open(input_dir + '/' + filename, 'U')
    dummy = infile.next() #remove header
    samplenames=infile.next().strip().split('\t')[1:] #get sample names
    data=[]
    for line in infile:
        data.append(line)
    infile.close()
    
    #transpose all data, and generate output filenames from sample names
    datamatrix=[]
    for line in data:
        datamatrix.append(line.strip().split('\t')[1:])
    tmatrix=zip(*datamatrix)
    outfilenames= ['CatchAll.' + sample + '.txt' for sample in samplenames]
    outfilepath= output_dir + "/" + filename.split('.txt')[0]
    os.mkdir(outfilepath)
    output_paths= []
        
    # for each sample, build a abundance,occurance pair, and then write this out to a txt
    for outfilename, sampletuple in zip(outfilenames, tmatrix):
        sample_histogram={}
        samplelist=list(sampletuple)
        
        #convert data from abundances to otu rank abundance histograms
        
        # for each otu count in a sample, enter into a dictionary the count, and the number of times seen
        for item in samplelist:
            sample_histogram[int(item)]=samplelist.count(item)
        #generate a tuple list of items and then sort the tuple
        sample_out=sample_histogram.items()
        sample_out.sort() #sorts on first element, the key, or the frequency count
        if sample_out[0][0]==0: #remove the 0,xxx line becuse catchall doesn't use it
            #print "zero line pruned in ", outfilename
            sample_out.pop(0)
        output_path = outfilepath + '/' + outfilename
        outfile=open(output_path,'w')
        for pair in sample_out:
            outfile.write(str(pair[0])+','+str(pair[1])+'\n')
        outfile.close()
        output_paths.append(output_path)
        print "writing to file: " + output_path + "\n"
    return output_paths

"""------------------------------------------------------------------------------------------"""

from string import strip
from optparse import OptionParser
import os

"""------------------------------------------------------------------------------------------"""
# Load files
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: python generate_CatchAll_infile.py -i input_directory",
                  description='4/13/12 JZL generate_CatchAll_infile.py')
    parser.add_option("-i", "--input_directory", action="store", type="string", dest="input_dir",
                  help="input directory of rarefaction files (txt format)")
    parser.add_option("-o", "--output_directory", action="store", type="string", dest="output_dir",
                  help="input directory of rarefaction files (txt format)")
    (options, args) = parser.parse_args()

    mandatories = ["input_dir", "output_dir"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nERROR: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    
    # read in command line args and parse path and files
    input_dir = "./"+options.input_dir
    output_dir = "./"+options.output_dir
    if not os.path.exists(input_dir):
        print "\nERROR: Input path does not exist\n"
        parser.print_help()
        exit(-1)
    elif os.path.exists(output_dir):
        print "\nERROR: Output path " + output_dir + " Exists!  Please remove.\n"
        parser.print_help()
        exit(-1)
    else:
        os.mkdir(output_dir)
        outfilenames = []
        listdir = os.listdir(input_dir)
        for filename in listdir:
            if '.txt' in filename:
                outfilenames = outfilenames + generate_catchall_file(input_dir, filename, output_dir)
    
    print "Writing output shell script. \n"
    shscript=open('CatchAll.sh','w')
    for outfilename in outfilenames:
        shscript.write('mono CatchAllCmdL.exe '+outfilename+' '+outfilename.split('.txt')[0]+'\n')
print "Done!"