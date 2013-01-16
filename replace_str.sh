#!/bin/bash
# NAME: replace_str.sh
# PURPOSE: replace all strings in a file given from a mapping table
# USAGE: replace_str.sh [-f file] [-t table] [-s separator] [-i column i] [-j column j] [-h]
# AUTHOR: Ye Yanbo
# DATE: 2013-01-15

USAGE="Usage: `basename $0` [-f file] [-t table] [-s separator] [-i column i] [-j column j] [-h]"
sep=","


if [ $# -eq 0 ]; then
	echo $USAGE >&2
	exit 1
fi

##get options
while getopts hf:t:s:i:j: o
do	case "$o" in
	h)	echo $USAGE; exit 0;;
	f)	file="$OPTARG";;
	t)	table="$OPTARG";;
	s)	sep="$OPTARG";;
	i)	columni="$OPTARG";;
	j)	columnj="$OPTARG";;
	[?])	echo $USAGE; exit 1;;
	esac
done

##read from $table and replace strings in $file
while read line
do
	str1=`echo $line | cut -d $sep -f $columni`
	str2=`echo $line | cut -d $sep -f $columnj`
	#echo  $str1 "to" $str2
	sed -i "s/$str1/$str2/g" $file
done < $table
