#!/bin/bash python
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sys
fn=sys.argv[1]
with open(fn +".faa", 'w') as aa_fa:
    for dna_record in SeqIO.parse(fn, 'fasta'):
        # use both fwd and rev sequences
        dna_seqs = [dna_record.seq]
        #dna_seqs = [dna_record.seq, dna_record.seq.reverse_complement()]

        # generate all translation frames
        aa_seqs = (s[0:].translate(to_stop=False) for s in dna_seqs)
        #aa_seqs = (s[i:].translate(to_stop=True) for i in range(3) for s in dna_seqs)

        # select the longest one
        #max_aa = max(aa_seqs, key=len)

        # write new record
        for seq in aa_seqs:
            aa_record = SeqRecord(seq, id=dna_record.id, description="")
            SeqIO.write(aa_record, aa_fa, 'fasta')
