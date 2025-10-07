#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created: Jackson Lee 2012

This script reads a list of positions and remaps them to the new position based 
on a mapping alignment file. This is use with remap_alignment.py to generate the 
*.mapping file. This file is used to help generate ecoli positions for SILVA 
mapping positions
   
mapping infile format:
1	1
2	1
3	1
4	2
5	3
etc
   
infile format:
1
1
3
5
etc
   
outfile format (infile.mapping):
1
1
1
3
etc

--------------------------------------------------------------------------------
usage:   remap_alignment.py -m ecoli.mapping -i chimera.window.txt
"""

#-------------------------------------------------------------------------------

#Header - Linkers, Libs, Constants

from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")

if __name__ == '__main__':
    parser = ArgumentParser(usage = "remap_alignment.py -m ecoli.mapping -i chimera.window.txt",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-m", "--mapping", action="store", dest="mappingfilename",
                  help="output from remap_alignment.py")
    parser.add_argument("-i", "--coords", action="store", dest="infilename",
                  help="alignment positions txt file")
    options = parser.parse_args()

    mandatories = ["mappingfilename", "infilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
mappingfilename= options.mappingfilename
infilename=options.infilename
outfilename= mappingfilename+'.remapped'

#open file


mappingdict={}
with open(mappingfilename,'U') as mappingfile:
    for line in mappingfile:
        mappingdictkey, mappingdictval=line.strip().split('\t')
        mappingdict[mappingdictkey]=mappingdictval

with open(infilename,'U') as infile, open(outfilename,'w') as outfile:
    for line in infile:
        lookupval=line.strip()
        remapval=mappingdict[lookupval]
        outline=str(remapval)+'\n'
        outfile.write(outline)

print("Done!")
