#!/usr/bin/env python
"""---------------------------------------------------------------------------------------"""
"""Jackson Lee 8/27/12"""
"""Read in lines of a fasta file and remove protein sequence new lines
   
    input file:
    fasta file 
    
    >gi|41178954|ref|NP_957541.1| putative mobilization protein A [Moraxella catarrhalis]
    MASFERTLMAGLNQDRYNILWVEHTDKDRLELNFLIPKVDLGTGKAMNPYFDKTDRGLVDVWKQVINYDYGLHDPDDPKN
    RQTLVTVKDLPKSKQEFKQALTAVLEQKILADEIKDHADIIKELENMGLEIARTTPTAISIKDPDGGRNIRLKGEIYEQT
    FTANQATERESQRASESYRNELEQRISRVRDELTSRIEAKSAFNATRYKTIPSREQSPNEQAHGIQDPSRGSNGDFVINP
    DSIRGVQSVLGQENSHTARAIRRYTTGDRQQPPTSQSTNESTGNGTGRQDLHRQQDEQSQNMAKQRQTTNHGATLNVKAI
    PERVRAIATRARTLLVIARDGKSDAQATDRAITATNSGLRDRKQQANDRKQRTVEIIGVAKNAGAGIDQHHAEQVRLQQQ
    QARQARQQTKDEPKKLGLDR
   
    output file:
    same, but without newlines
   
    usage:
    python fix_refseq_faa.py -i input.fasta -o outfilename.fasta

    """
"""---------------------------------------------------------------------------------------"""
"""Header - Linkers, Libs, Constants"""
from string import strip
from re import split
from optparse import OptionParser

"""function declarations"""

"""---------------------------------------------------------------------------------------"""
"""Body"""
print "Running..."


if __name__ == '__main__':
    parser = OptionParser(usage = "usage:  python fix_refseq_faa.py -i input.fasta -o outfilename.fasta",                  
    description='8/27/12 JZL fix_refseq_faa.py.  Read in FASTA and remove sequence newlines (see docstring for format).  Useful for very large files.')
    parser.add_option("-i", "--input_fasta", action="store", type="string", dest="inputfilename",
                  help="fasta file of input sequences")
    parser.add_option("-o", "--outfile_filter", action="store", type="string", dest="outfilename",
                  help="output fasta file name")    
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename", "outfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    
    # read in command line args and parse file
    inputfilename = options.inputfilename
    outfilename=options.outfilename
    
    infile = open(inputfilename, 'U')
    outfile = open(outfilename, 'w')  

    for linenum, line in enumerate(infile):
        if line[0] == ">":
            if linenum != 0:
                outline = "\n" + line
            else:
                outline = line[:]
            outfile.write(outline)
        elif line.strip().isupper():
            outfile.write(line.strip())
    print str(linenum)+" lines written"
    infile.close()
    outfile.close()

    print "Done!"