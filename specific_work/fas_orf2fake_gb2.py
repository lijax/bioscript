'''
Created on 2012-12-5

@author: yeyanbo
'''


from Bio import SeqIO
from Bio.Alphabet.IUPAC import IUPACUnambiguousDNA
from Bio.SeqFeature import SeqFeature, FeatureLocation

fas_gn = "/home/yeyanbo/baculovirus/new_sequenced_genomes/Clostera anastomosis GV-complete genome.fas"
orf_tb = "/home/yeyanbo/baculovirus/new_sequenced_genomes/Clostera anastomosis GV-complete genome.cds"
gb_gn = "/home/yeyanbo/baculovirus/new_sequenced_genomes/Clostera anastomosis GV-complete genome.gb"

fas_gn_file = open(fas_gn, "r")
orf_tb_file = open(orf_tb, "r")
gb_gn_file = open(gb_gn, "w")

gb_record = []

for seq_record in SeqIO.parse(fas_gn_file, "fasta") :
    print "Dealing with GenBank record %s" % seq_record.id
    
    seq_record.seq.alphabet = IUPACUnambiguousDNA()

    seq_record.id = 'LC_000002.1'
    seq_record.name='LC_000002'
    seq_record.description = 'Clostera anastomosis GV, complete genome.'
    
    seq_record.annotations["taxonomy"] = ['Viruses', 'dsDNA viruses, no RNA stage', 'Baculoviridae', 'unclassified GV']
    seq_record.annotations["sequence_version"] = 1
    seq_record.annotations["source"] = 'Clostera anastomosis GV'
    seq_record.annotations["keywords"] = ['']
    seq_record.annotations["accessions"] = ['LC_000002']
    seq_record.annotations["gi"] = '000000002'
    seq_record.annotations["data_file_division"] = 'VRL'
    seq_record.annotations["organism"] = 'Clostera anastomosis GV'
    seq_record.annotations["date"] = '05-DEC-2012'
    
    source_feature = SeqFeature(FeatureLocation(0, len(seq_record.seq), strand=1), type='source')
    
    source_feature.qualifiers["host"] = ['Clostera anastomosis.']
    source_feature.qualifiers["mol_type"] = ['genomic DNA']
    source_feature.qualifiers["organism"] = ['Clostera anastomosis GV']
    source_feature.qualifiers["country"] = ['China: Wuhan, Hubei']
    
    seq_record.features.append(source_feature)
    
    count = 0;
    for line in orf_tb_file:
        count += 1;
        cds_num = map(int, line.split('\t'))
        cds_seq = seq_record.seq[cds_num[1] - 1:cds_num[2]]
        std = 1
        if cds_num[0] < 0:
            cds_seq = cds_seq.reverse_complement()
            std = -1
            
        cds_translate = str(cds_seq.translate())
        cds_translate = cds_translate[0:len(cds_translate)-1]
        cds_feature = SeqFeature(FeatureLocation(cds_num[1] - 1, cds_num[2], strand = std), type = "CDS")
        cds_feature.qualifiers["locus_tag"] = ['CAGV' + str(count).zfill(3)]
        cds_feature.qualifiers["codon_start"] = ['1']
        cds_feature.qualifiers["product"] = ['unknown']
        cds_feature.qualifiers["note"] = ['unknown']
        cds_feature.qualifiers["db_xref"] = ['GI:200000' + str(count).zfill(3)]
        cds_feature.qualifiers["translation"] = [cds_translate]
        cds_feature.qualifiers["protein_id"] = ['LP_200000' + str(count).zfill(3)]
        
        seq_record.features.append(cds_feature)
        
    gb_record.append(seq_record)
    
SeqIO.write(gb_record, gb_gn_file, "genbank")

fas_gn_file.close()
orf_tb_file.close()
gb_gn_file.close()  