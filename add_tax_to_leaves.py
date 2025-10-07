#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:  Jackson Lee 8/27/12

Read in phyloxml file or a tog newick tree file and a fasta file and match top 10 
characters of header with xml.  Then add in the appropriate genome name
    
input file:
fasta file 
    
>gi|41178954|ref|NP_957541.1| putative mobilization protein A [Moraxella catarrhalis]
MASFERTLMAGLNQDRYNILWVEHTDKDRLELNFLIPKVDLGTGKAMNPYFDKTDRGLVDVWKQVINYDYGLHDPDDPKN
RQTLVTVKDLPKSKQEFKQALTAVLEQKILADEIKDHADIIKELENMGLEIARTTPTAISIKDPDGGRNIRLKGEIYEQT
FTANQATERESQRASESYRNELEQRISRVRDELTSRIEAKSAFNATRYKTIPSREQSPNEQAHGIQDPSRGSNGDFVINP
DSIRGVQSVLGQENSHTARAIRRYTTGDRQQPPTSQSTNESTGNGTGRQDLHRQQDEQSQNMAKQRQTTNHGATLNVKAI
PERVRAIATRARTLLVIARDGKSDAQATDRAITATNSGLRDRKQQANDRKQRTVEIIGVAKNAGAGIDQHHAEQVRLQQQ
QARQARQQTKDEPKKLGLDR
   
xml file:
<?xml version="1.0" encoding="UTF-8"?>
...
<clade><name>307718067|</name><branch_length>0.291147</branch_length><color>
<red>255</red><green>90</green><blue>90</blue></color></clade></clade>
...
    
newick tree file:
(333980686|:0.0841434,((((317133238|:0.208684,((20090069|r:1.25081e-06,20090077|r:1.25081e-06):0.0181263,73669771|
r:0.135455):0.126873):0.0860154,153954373|:0.224343):0.051196,(((313203840|:0.211795,193215533|:0.172569):0.0712309,
(345860857|:0.158235,(392959144|:0.0539456,(325290943|:0.0749888,359413714|:0.0651864):0.0201283):0.0342632):0.0100293):
0.0420961,((374812684|:0.126264,379010572|:0.0514746):0.0344013,(((225164851|:0.0179084,((373853634|:1.25081e-06,390119243
|:1.25081e-06):1.25081e-06
    
output file:
filename: inputfile.taxadded.xml
    
same xml, but with gi and genome added in
    
--------------------------------------------------------------------------------
usage:    python add_tax_to_leaves.py -i input.fasta -x phylo.xml -n
"""
#-------------------------------------------------------------------------------
#Header - Linkers, Libs, Constants
from string import strip
from re import split
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#-------------------------------------------------------------------------------
#function declarations

#-------------------------------------------------------------------------------
#Body
print("Running...")


if __name__ == '__main__':
    parser = ArgumentParser(usage = "python add_tax_to_leaves.py -i input.fasta -x phylo.xml",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fasta", action="store", 
                        dest="inputfilename",
                        help="fasta file of input sequences")
    parser.add_argument("-x", "--xml_file", action="store", dest="xmlfilename",
                        help="output fasta file name")  
    parser.add_argument("-n", "--newick_file", action="store_true", 
                        dest="NewickFlag", help="set for newick file")                  
    options = parser.parse_args()

    mandatories = ["inputfilename", "xmlfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
    
    # read in command line args and parse file
    inputfilename = options.inputfilename
    xmlfilename = options.xmlfilename
    newickflag = options.NewickFlag
    
    if newickflag:
        outfilename= xmlfilename.strip().split('.tre')[0]+".taxadded.tre"
    else:
        outfilename= xmlfilename.strip().split('.xml')[0]+".taxadded.xml"

    
    infile = open(inputfilename, 'U')
    xmlfile = open(xmlfilename, 'U')
    outfile = open(outfilename, 'w')  
    
    if newickflag:
        secondline = xmlfile.next()
    else:
        firstline = xmlfile.next()
        secondline = xmlfile.next()
    xmlfile.close()

    for line in infile:
        if line[0] == ">":
            tag = line[1:11]
            gi = line.strip().split("|")[0][1:]
            genomename = line.strip().split("[")[1][0:-1]
            if newickflag:
                secondline = secondline.replace(tag, gi.replace(" ","_") + "_" + genomename.replace(" ","_"))            
            else:
                secondline = secondline.replace(tag, gi + " " + genomename)
    infile.close()
    
    if newickflag:
        outfile.write(secondline)
    else:
        outfile.write(firstline)
        outfile.write(secondline)
    outfile.close()

    print(outfilename + " written.")

    print("Done!")
