'''
Created on 2012-11-7

@author: yeyanbo
'''
import re
from Bio import SeqIO

fr = open("/home/yeyanbo/baculovirus_new/68_all_Genomes.gb", 'a')
for seq_record in SeqIO.parse("/home/yeyanbo/baculovirus_new/124_Genomes.gb", "genbank"):
    print seq_record.id
    print repr(seq_record.seq)
    print len(seq_record)
    
    if not re.match('NC_.*', seq_record.id, 0):
        SeqIO.write(seq_record, fr , "genbank")

fr.close()
