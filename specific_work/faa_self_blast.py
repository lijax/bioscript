#! /usr/bin/env python
'''
Created on 2012-11-7

@author: yeyanbo
'''

import os
from Bio.Blast.Applications import NcbipsiblastCommandline


faa = "/home/yeyanbo/baculovirus_new/56_ref_Genomes.faa"
cmd = "formatdb -i %s -p T " % faa
os.system(cmd)

blastx_cline = NcbipsiblastCommandline(query=faa, db=faa, outfmt=5, out="%s.xml" % faa)

stdout, stderr = blastx_cline()
