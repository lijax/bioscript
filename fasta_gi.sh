#!/bin/bash
# NAME: fasta_gi.sh
# PURPOSE: remove all information in fasta header  except GI number and save the header information in a table
# USAGE: fasta_gi.sh [-i input file] [-o output file] [-t header info file] [-h]
# AUTHOR: Ye Yanbo
# DATE: 2013-01-15

##get options
USAGE="Usage: `basename $0` [-i input file] [-o output file] [-t header info file] [-h]"

if [ $# -eq 0 ]; then
	echo $USAGE >&2
	exit 1
fi

while getopts hi:o:t: opt
do	case "$opt" in
	h)	echo $USAGE; exit 0;;
	i)	infile="$OPTARG";;
	o)	outfile="$OPTARG";;
	t)	csvfile="$OPTARG";;
	\?)	echo $USAGE; exit 1;;
	esac
done


> "$outfile" 
> "$csvfile" 

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

grep ">" $outfile | sed 's/^>gi|\([0-9]*\)|\([a-z]*\)|\([A-Z]*_[0-9]*\)\.[0-9]*| \(.*\) \[\(.*\)\]$/\1,\3,\4,\5/g' > $csvfile
sed -i 's/>gi|\([0-9]*\)|.*/>\1/g' $outfile