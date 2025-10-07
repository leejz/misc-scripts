#!/usr/bin/env python
### script to convert a clustal format input that comes from pymol aligmnet, extract alignment consensus mask and output as a gff track file

from Bio import AlignIO
from Bio import SeqIO
from argparse import ArgumentParser, RawDescriptionHelpFormatter

#Body

if __name__ == '__main__':
    parser = ArgumentParser(usage = "python convert_pymol.py -i clustal.aln",
                            description=__doc__,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input_clustal", action="store",
                        dest="input_clustal",
                        help="clustal format alignment file")
    parser.add_argument("-f", "--offset", action="store", dest="offset", default=1,
                        help="gff bp offset")
    parser.add_argument("-n", "--seq_no", action="store", dest="seq_id", default=0, type=int,
                        help="which sequence fa to output")
    options = parser.parse_args()

    mandatories = ["input_clustal"]
    for m in mandatories:
        if not options.__dict__[m]:
            print("\nERROR: Missing Arguments\n")
            parser.print_help()
            exit(-1)

    cw_prefix = options.input_clustal.rpartition('.')[0]
    fa_prefix = cw_prefix.split('/')[-1]
    cw = AlignIO.read(options.input_clustal, format="clustal")
    cw_con = cw.column_annotations["clustal_consensus"].replace(".", "*")
    # generate tracks
    curbp = int(options.offset)
    cw_words = cw_con.split(' ')
    track_linea =  '\t'.join([fa_prefix, "pymol", "conserved structure", ''])
    track_lineb = '\t'.join(['', '.', '+', '.',''])
    snp_track = [i==j for i,j in zip(cw[0].seq,cw[1].seq)]
    track_lineas =  '\t'.join([fa_prefix, "pymol", "SNP", ''])
    track_linebs = '\t'.join(['', '.', '+', '.',''])
    with open(cw_prefix+'.gff', 'w') as ofh:
        for word in cw_words:
            lastbp = curbp
            if word == '':
                curbp = curbp+1
            else:
                curbp = curbp + len(word) +1
                ofh.write(track_linea + str(lastbp)+'\t'+str(curbp-2) + track_lineb + "ID=conserved structure\n")
        for bp, snp_tf in enumerate(snp_track):
            if not snp_tf: 
                ofh.write(track_lineas + str(bp+1) + '\t' + str(bp+1) + track_linebs + "ID=SNP\n")

    outrec = cw[options.seq_id]
    outrec.id = fa_prefix
    outrec.name = ''
    outrec.description = ''
    with open(cw_prefix+'.fa', 'w') as fofh:
        SeqIO.write(outrec, fofh, "fasta")
