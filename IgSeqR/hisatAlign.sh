#!/bin/bash

## Parse arguments
cores=$1
indexedRef=$2
outDir=$3
unpaired=$4
input1=$5
input2=$6

if $unpaired == "No"
then
## HISAT2 alignment - Paired Mode
hisat2 -p $cores --phred33 -t -x $indexedRef -1 $input1 -2 $input2 | \
  samtools sort -O BAM | \
  tee ./hisat2/hisat2_output.bam | \
  samtools index - ./hisat2/hisat2_output.bam.bai
else
## HISAT2 alignment - Unpaired Mode
hisat2 -p $cores --phred33 -t -x $indexedRef -U $input1 | \
  samtools sort -O BAM | \
  tee "$outDir"/hisat2_output.bam | \
  samtools index - "$outDir"/hisat2_output.bam.bai
fi
