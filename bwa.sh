#!/bin/bash
#$ -S /bin/bash
#$ -cwd

#qsub bwa.sh read10000 ref/ecoli_index

PREFIX=$1 # read10000
REFFILE=$2 # ref/ecoli_index

bwa mem  ${REFFILE}   ${PREFIX}.fastq > ${PREFIX}.sam
#bwa mem  read10000   read10000.fastq > read10000.sam

#bwa aln ${REFFILE} ${PREFIX}.fastq > ${PREFIX}.sai
#bwa samse ${REFFILE} ${PREFIX}.sai ${PREFIX}.fastq > ${PREFIX}.sam
