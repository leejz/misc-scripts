#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
Created:   Jackson Lee 5/19/12
This script reads in a fasta file of picked otus and the same otu table and 
outputs the UChime de novo input file for Usearch
   
Input fasta file format:
denoised_all.fasta_rep_set.rc.fasta
   
>0
GTCGAGCGCAGATGGAGGTGACACAAGCGGATAAGAGAACAGAATGCGAAGCATTCTTTTCCTTTTGTATTCTTTGTGT
   
Input OTU table format:
denoised_otu_table.txt
   
# QIIME v1.2.1-dev OTU table
#OTU ID Aeb.1   Aeb.2A  Aeb.2B  Eq.1    Eq.3    Eq.42   Eq.5    In.1    In.3    
0       0       0       0       0       0       0       0       0       0

Output file format:
>0 /ab=xxx/ 
GTCGAGCGCAGATGGAGGTGACACAAGCGGATAAGAGAACAGAATGCGAAGCATTCTTTTCCTTTTGTATTCTTTGTGT

--------------------------------------------------------------------------------
denovo_parser.py -i input_file.fasta -n input_otu_table.txt
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
    parser = ArgumentParser(usage = "denovo_parser.py -i input_file.fasta -n \
input_otu_table.txt",
                            description=__doc__, 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_fasta", action="store", 
                        dest="inputfilename",
                        help="fasta file of input sequences")
    parser.add_argument("-n", "--input_otutable", action="store", 
                        dest="inputotuname", help="input otu table")
    options = parser.parse_args()

    mandatories = ["inputfilename", "inputotuname"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nError: Missing Arguments\n")
            parser.print_help()
            exit(-1)
            
    fastafilename = options.inputfilename
    otufilename = options.inputotuname
    outfilename = fastafilename.split('.fasta')[0]+'.denovo_uchime.fasta'
    print("Otu table processing...")
    otuinfile = open(otufilename,'U')

    #junk the first 2 rows
    otuinfile.next()
    otuinfile.next()

    abs_abundances = []
    otunames = []
    for line in otuinfile:
        pars = line.strip().split('\t')
        otunames.append(pars[0])
        abs_abundances.append(sum(map(int,pars[1:-1])))

    otuinfile.close()

    max_abund = sum(abs_abundances)
    rel_abundances = []
    for i in abs_abundances:
        rel_abundances.append(float(i)/max_abund*100)

    abund_dict={}
    for otuname, rel_abund in zip(otunames,rel_abundances):
        abund_dict[otuname]=rel_abund

    print("Fasta file processing...")
    fastainfile=open(fastafilename,'U')
    outfile=open(outfilename,'w')

    for line in fastainfile:
        if line[0] == '>': # if line is a header
            otuheader = line.strip().split(' ')[0][1:]
            outfile.write('>'+otuheader+' /ab=%.8f/ \n' % abund_dict[otuheader])
        else:
            outfile.write(line)
        
    fastainfile.close()
    outfile.close()

    print("Done!")
