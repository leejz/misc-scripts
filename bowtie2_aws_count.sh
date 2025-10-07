#!/bin/bash

#script to copy from s3 a single file, run bowtie2, and save an output count file. requires aws cli

ref_path=$1
s3fq1=$2
gff=$3
outpath=$4
s3fq2=${s3fq1%R1_001.fastq.gz}R2_001.fastq.gz
fq1=$(basename $s3fq1)
fq2=$(basename $s3fq2)
sn=${fq1%_R1_001.fastq.gz}
tmpdir=$(mktemp -d -t $sn)
echo aws s3 cp $s3fq1 $tmpdir/
echo aws s3 cp $s3fq2 $tmpdir/

cmd="bowtie2_count.sh $ref_path $tmpdir/$fq1 $tmpdir/$fq2 $gff $outpath"
echo $cmd
#eval $cmd

#rm -r $tmpdir
