#!/bin/bash
# NAME: all2all_blast.sh
# PURPOSE: to do all2all blast iteratively with different parameters and generate different xml files
# USAGE: all2all_blast.sh [-i input file] [-o output file] [-h]
# AUTHOR: Ye Yanbo
# DATE: 2013-04-21

##get options
##USAGE="Usage: `basename $0` [-i input file] [-o output file] [-c cpu number] [-h]"
USAGE="Usage: `basename $0` [-p program] [-i input file] [-o output file] [-h]"

if [ $# -eq 0 ]; then
	echo $USAGE >&2
	exit 1
fi

while getopts hi:o:c:p: opt
do	case "$opt" in
	h)	echo $USAGE; exit 0;;
	p)  program="$OPTARG";;
	i)	infile="$OPTARG";;
	o)	outfile="$OPTARG";;
#	c)  cpu="$OPTARG";;
	\?)	echo $USAGE; exit 1;;
	esac
done

matrices="BLOSUM80 BLOSUM62 BLOSUM50 BLOSUM45 PAM250 BLOSUM90 PAM30 PAM70"

formatdb -i $infile

for matrix in $matrices; do
	echo ${matrix}"..."
	$program -query $infile -db $infile -out ${outfile}"_"${matrix}".xml" -matrix $matrix -outfmt 5
	echo ${matrix}" complete"
done