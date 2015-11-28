#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 5/19/12
   
This script reads a tab file containing reference taxonomy and a file containing 
classified taxonomy and compares each rank. The script outputs how many of the 
comparison matches 
   
input:
a file of taxonomies with the format:
OrySativ Bacteria;Proteobacteria;Alphaproteobacteria;unclassified;
MarMet17 Bacteria;Proteobacteria;Gammaproteobacteria;unclassified;
etc.
   
 NOTE: files may need to be parsed into this format from other formats

Output:
a listing of each taxonomic rank and the number of matches, and the total 
number of entries examined.

--------------------------------------------------------------------------------
usage:  tax_rank_comparison.py -t classified.taxonomy -T reference.taxonomy
"""
#-------------------------------------------------------------------------------
#Functions & Declarations
    
from string import strip
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#Body
print "Running..."

if __name__ == '__main__':
    parser = ArgumentParser(usage = "tax_rank_comparison.py -t classified.taxonomy -T reference.taxonomy",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-t", "--classified_tax", action="store", 
                        dest="classtaxname",
                        help="classified taxonomy file")
    parser.add_argument("-T", "--reference_tax", action="store", 
                        dest="reftaxname",
                        help="reference taxonomy file")
    options = parser.parse_args()

    mandatories = ["reftaxname", "classtaxname"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    
    # read in command line args and parse file
    reffilename = options.reftaxname
    reffile = open(reffilename, 'U')
    classfilename = options.classtaxname
    classfile = open(classfilename, 'U')
    
    count = 0
    unmatched = 0
    match_rank_list = [0]*15
    ref_rank_list =  [0]*15
    class_rank_list =  [0]*15
    
    #read in each line of each file
    for refline, classline in zip(reffile, classfile):
        #parse each line
        refname, space, reftax = refline.strip().partition(' ')
        classname, space, classtax = classline.strip().partition(' ')
        reflist = reftax.strip(';').split(';')
        classlist = classtax.strip(';').split(';')
        count += 1
        
        #verify names are the same and then compare each level
        if refname.strip() == classname.strip():
            reflen = len(reflist)
            classlen = len(classlist)
            minlen = min(reflen, classlen)
            # error if rank is greater than the match list size
            if minlen >= len(match_rank_list):
                #unmatched += 1
                print 'foo'
            else:
                for taxrank in range(minlen):
                    if (reflist[taxrank] == classlist[taxrank]) and (reflist[taxrank] != 'unclassified'):
                        match_rank_list[taxrank] += 1
                for taxrank in range(reflen):
                    if reflist[taxrank] != 'unclassified':
                        ref_rank_list[taxrank] +=1
                for taxrank in range(classlen):
                    if classlist[taxrank] != 'unclassified':
                        class_rank_list[taxrank] +=1
        else:
            unmatched += 1

    reffile.close()
    classfile.close()
    
    #Output data
    print 'reference taxonomy:\t\t'+reffilename
    print 'classification taxonomy:\t'+classfilename
    print 'Matches found at each taxonomic rank'
    print '------------------------------------'
    print 'Taxonomic Rank:\t'+'\t '.join(map(str,range(len(match_rank_list))))
    print '\t\t'+'\t '.join(map(str,match_rank_list))
    print 'Total entries:\t'+str(count)+'\n\n'
    print 'Taxonomic ranks in reference taxonomy'
    print '------------------------------------'
    print 'Taxonomic Rank:\t'+'\t '.join(map(str,range(len(ref_rank_list))))
    print '\t\t'+'\t '.join(map(str,ref_rank_list))
    print 'Total entries:\t'+str(count)+'\n\n'
    print 'Taxonomic ranks in classified taxonomy'
    print '------------------------------------'
    print 'Taxonomic Rank:\t'+'\t '.join(map(str,range(len(class_rank_list))))
    print '\t\t'+'\t'.join(map(str,class_rank_list))
    print 'Total entries:\t '+str(count)+'\n\n'
    print 'unmatched:\t'+str(unmatched)
print "Done!"