#! /usr/bin/env python
#   
# python script template file
#
# @data: 2013-2-2
# @author: yeyanbo

##import other module
import getopt
import sys

def usage():
    """ modify this for usage information"""

    usage = """Usage: python script.py -i [input file] -o [output file]
    
Option:
  -h,--help      Print this usage
  -i,--input     input file
  -o,--output    output file
"""
    print usage

def main():
    """ main work flow should be in the main function"""

    #get options and arguments
    #modify options to your version as described in the usage() function
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:h", ["input=", "output=", "help"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    #default value of options and arguments
    #modify default value to your version
    infile = None
    outfile = None

    #parse options
    #modify this accordingly
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            infile = a
        elif o in ("-o", "--output"):
            outfile = a
        else:
            assert False, "unhandled option"

    #check options and print usage if unexpected 
    #modify this accordingly
    if infile == None or outfile == None:
        usage()
        sys.exit(2)

    #real work flow goes here
    print "input file is '%s' and output file is '%s'" % (infile, outfile)

if __name__ == "__main__":
    main()