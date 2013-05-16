#!/bin/bash
# NAME: fasta_header.sh
# PURPOSE: remove all information in fasta header except needed one define by a given number and save the header information in a table
# USAGE: fasta_header.sh [-i input file] [-o output file] [-n info number] [-t header info file] [-h]
# AUTHOR: Ye Yanbo
# DATE: 2013-05-16

##get options
USAGE="Usage: `basename $0` [-i input file] [-o output file] [-n info number] [-t header info file] [-h]"

if [ $# -eq 0 ]; then
	echo $USAGE >&2
	exit 1
fi

outfile="output.fasta"
num=1

while getopts hi:o:n:t: opt
do	case "$opt" in
	h)	echo $USAGE; exit 0;;
	i)	infile="$OPTARG";;
	o)	outfile="$OPTARG";;
	n)	num="$OPTARG";;
	t)	csvfile="$OPTARG";;
	\?)	echo $USAGE; exit 1;;
	esac
done

if [ ! $infile ]; then
	echo $USAGE
	exit 1
fi

> "$outfile"  

while read line
do
	f=`echo ${line:0:1}`
	if [ "$f" == ">" ]; then
		str=`echo $line | cut -d ">" -f 2`
		echo ">$str" >> $outfile
	else
		echo $line >> $outfile
	fi
done < $infile

if [ "$csvfile" != "" ]; then
	> "$csvfile"
	grep ">" $outfile | sed 's/^>gi|\([0-9]*\)|\([a-z]*\)|\([A-Z]*_[0-9]*\)\.[0-9]*| \(.*\) \[\(.*\)\]$/\1,\3,\4,\5/g' > $csvfile
fi

sed -i "s/^>gi|\([0-9]*\)|\([a-z]*\)|\([A-Z]*_[0-9]*\)\.[0-9]*| \(.*\) \[\(.*\)\]$/>\\$num/g" $outfile
