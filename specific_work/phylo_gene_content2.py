'''
Created on 2013-01-15
modified to create itol branch label file which is to show gene numbers in each branch
@author: yeyanbo
'''
from random import shuffle
from Bio import Phylo
from Bio.Phylo.PhyloXML import Phylogeny
import csv

#tree_file = "/home/yeyanbo/baculovirus_new/core_fasta/merge.bionj.tree"
tree_file = "/home/yeyanbo/baculovirus_new/testresult.tree"
gene_data = "/home/yeyanbo/baculovirus_new/bac_56_gene_content.csv"
phylo_gene_result = "/home/yeyanbo/baculovirus_new/56_phylo_gene_label"

tree = Phylo.read(tree_file, "newick")
data = csv.reader(open(gene_data), delimiter = ',')
phylo_gene_file = open(phylo_gene_result, "w")

data_columns = zip(*data)

#print data_columns[0]

data_dic = {}
# for i in range(0,len(data_columns) - 1):
#     data_dic[data_columns[i][0]] = data_columns[i][1:]

data_dic = {data[0] : [int(n) for n in data[1:]] for data in data_columns}

#share = [True for g in zip(data_dic["AcNPV"], data_dic["RoMNPV"]) if all(g)]

clade_dic = {}
clades_inner = tree.get_nonterminals()
for clade in clades_inner:
	terms = []
	data_list = []
	for term in clade.get_terminals():
		  term_name = term.name
		  terms.append(term_name)
		  data_list.append(data_dic[term_name])
	share = [True for g in zip(*data_list) if all(g)]
	clade_dic["|".join(terms)] = len(share)

for clade in clades_inner:
	terms_cur = []
	terms_pre = []
	clade_pre = [clade_tmp for clade_tmp in clades_inner if clade in clade_tmp]
	num_cur = 0
	num_pre = 0
	if clade_pre:
		for term in clade_pre[0].get_terminals():
			  term_name = term.name
			  terms_pre.append(term_name)
		num_pre = clade_dic.get("|".join(terms_pre))

	for term in clade.get_terminals():
		  term_name = term.name
		  terms_cur.append(term_name)
	num_cur = clade_dic.get("|".join(terms_cur))
	shuffle(terms_cur)
	#phylo_gene_file.write("|".join(terms_cur))
	phylo_gene_file.write("%s\t%s/%s/%s\t#ff0000\n" % (clade.name, num_cur - num_pre, num_pre, num_cur))

clades_ter = tree.get_terminals()
for clade in clades_ter:
	terms_cur = []
	terms_pre = []
	num_cur = 0
	num_pre = 0
	clade_pre = [clade_tmp for clade_tmp in clades_inner if clade in clade_tmp]
	if clade_pre:
		for term in clade_pre[0].get_terminals():
			  term_name = term.name
			  terms_pre.append(term_name)
		num_pre = clade_dic.get("|".join(terms_pre))

	for term in clade.get_terminals():
	  term_name = term.name
	  terms_cur.append(term_name)
	num_cur = len([True for g in data_dic[term_name] if g])
	phylo_gene_file.write("%s\t%s/%s/%s\t#ff0000\n" % (term_name, num_cur - num_pre, num_pre, num_cur))



phylo_gene_file.close()