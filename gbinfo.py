#! /usr/bin/env python
#   
# Extract genome information(length, gc, etc.)
# @date: 2013-04-02
# @author: yeyanbo

import re
import getopt
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import SeqUtils
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet.IUPAC import unambiguous_dna, ambiguous_dna
from Bio.Alphabet import generic_protein
from Bio.SeqUtils.CodonUsage import CodonAdaptationIndex

def usage():
    usage = """Usage: python gb2fasta.py -i [input file] -o [output file]
    
Option:
  -h,--help      Print this usage
  -v,--verbose   Print progress information
  -i,--input     The genbank file to be processed
  -o,--output    The fasta file to be output to
"""

    print usage

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:hv", ["input=", "output=", "help"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    infile = None
    outfile = None
    verbose = False


    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            infile = a
        elif o in ("-o", "--output"):
            outfile = a
        else:
            assert False, "unhandled option"

    if infile == None or outfile == None:
        usage()
        sys.exit(2)


    input_handle = open(infile, "r")
    output_handle = open(outfile, "w")
    caIndex = CodonAdaptationIndex() 
    #output_handle.write("Accession, GI, Organism, Taxonomy, Length, GC, ORF, CodingLength, CodingPercentage, CodingGC, CodingGC1, CodingGC2, CodingGC3, CAI\n")
    output_handle.write("Accession, GI, Organism, Taxonomy, Length, GC, ORF, CodingLength, CodingPercentage, CodingGC, CodingGC1, CodingGC2, CodingGC3\n")
    for seq_record in SeqIO.parse(input_handle, "genbank") :
        gb_id = seq_record.id
        gb_gi = seq_record.annotations['gi']
        gb_dec = seq_record.description

        if verbose:
            print "Record %s" % gb_id

        organism = seq_record.annotations["organism"]
        taxonomy = seq_record.annotations["taxonomy"]
        gc_content = SeqUtils.GC(seq_record.seq);
        length = len(seq_record);
        cds_count = 0 # count CDS in current record
        concat_CDSs = Seq("", ambiguous_dna)
        for seq_feature in seq_record.features :
            if seq_feature.type == "CDS" :
                assert len(seq_feature.qualifiers['translation']) == 1
                
                cds_count += 1 
                
                strand = seq_feature.strand
                
                location = str(seq_feature.location.start + 1) + "-" + str(seq_feature.location.end)

                seq = seq_record.seq[seq_feature.location.start:seq_feature.location.end]
                if strand == -1:
                   seq = seq.reverse_complement()

                concat_CDSs = concat_CDSs + seq
        
        length_CDSs = len(concat_CDSs)
        gc_CDSs = SeqUtils.GC123(concat_CDSs)

        coding_percentage = 1.0 * length_CDSs / length
        #cai = caIndex.cai_for_gene(str(concat_CDSs))
        
        #output_handle.write(re.sub(r"\.\d+", "", gb_id) + ", " + gb_gi + ", " + organism + ", " + ";".join(taxonomy) + ", " + str(length) + ", " + str("%.2f" % gc_content) + ", " + str(cds_count) + ", " + str(length_CDSs) + ", " + str("%.2f" % coding_percentage)  + ", " + ", ".join(str("%.2f" % x) for x in gc_CDSs) + "," + str("%.2f" % cai) + "\n")
        #output_handle.write(re.sub(r"\.\d+", "", gb_id) + ", " + gb_gi + ", " + organism + ", " + taxonomy[3] + ", " + str(length) + ", " + str("%.2f" % gc_content) + ", " + str(cds_count) + ", " + str(length_CDSs) + ", " + str("%.2f" % coding_percentage)  + ", " + ", ".join(str("%.2f" % x) for x in gc_CDSs) + "," + str("%.2f" % cai) + "\n")
        #output_handle.write(re.sub(r"\.\d+", "", gb_id) + ", " + gb_gi + ", " + organism + ", " + ";".join(taxonomy) + ", " + str(length) + ", " + str("%.2f" % gc_content) + ", " + str(cds_count) + ", " + str(length_CDSs) + ", " + str("%.2f" % coding_percentage)  + ", " + ", ".join(str("%.2f" % x) for x in gc_CDSs) + "," + "\n")
        output_handle.write(re.sub(r"\.\d+", "", gb_id) + ", " + gb_gi + ", " + organism + ", " + taxonomy[3] + ", " + str(length) + ", " + str("%.2f" % gc_content) + ", " + str(cds_count) + ", " + str(length_CDSs) + ", " + str("%.2f" % coding_percentage)  + ", " + ", ".join(str("%.2f" % x) for x in gc_CDSs) + "," + "\n")
    output_handle.close()
    input_handle.close()


if __name__ == "__main__":
    main()

