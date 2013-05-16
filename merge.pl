#! /usr/bin/perl -w
## 2012.5.29 lina
use Bio::SeqIO;

my $input1 =shift @ARGV;
my $out =Bio::SeqIO ->new (-file => ">merge.fasta", -format =>"fasta");

#build a hash using input file 1
$in1 =Bio::SeqIO ->new (-file =>$input1, -format =>"fasta");
my %hash;
while (my $seq1 = $in1 ->next_seq() ) {
	$hash{$seq1 ->display_id}=$seq1->seq;
}

for (@ARGV){
	#search file 2 in hash
	my $in2 =Bio::SeqIO ->new (-file =>$_, -format =>"fasta");
	while (my $seq2 = $in2 ->next_seq() ){
		my $acc = $seq2 ->display_id;
		if (exists $hash{$acc}) {
			#add the %hash value
			$hash{$acc}.=$seq2->seq;
		}
	}
}

#print %hash
for $acc (sort keys %hash){
	my $seq_obj = Bio::Seq ->new (
	  	                        -seq => $hash{$acc},
 	 		                     -display_id => $acc,
  		  	                     );
	$out -> write_seq($seq_obj);
}
