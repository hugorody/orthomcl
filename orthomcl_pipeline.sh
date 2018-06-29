#OrthoMCL installation

workingdir="/home/hugo/Documents/orthomcltest"
orthodir=`echo "$workingdir/orthomclSoftware-v2.0.9/bin"`
mysqlpass="user123"
dependenciesinstall="no"
installorthomcl="no"
fastainput="/home/hugo/Desktop/orthomcl/seqs_in_table.fas"
taxon="Sugar"
intlog="1"
clusteracro="SUG"
blastAVAfile="" #blast all-vs-all file - if not provided will run

#/home/hugo/Documents/orthomcltest/orthomclSoftware-v2.0.9/my_orthomcl_dir/all-vs-all.blastp

#STEP (1)
#install or get access to a supported relational database.  If using MySql, certain configurations are required, so it may involve working with your MySql administrator or installing your own MySql.  See the mysqlInstallationGuide.txt document provided with the orthomcl software.

if [ "$dependenciesinstall" = "yes" ]; then
    echo "Installing dependencies..."
  sudo apt-get install libxi-dev libxmu-dev freeglut3-dev libgsl0-dev libnetpbm10-dev libplplot-dev pgplot5 build-essential gfortran

  cpanm BioPerl DBI Parallel::ForkManager YAML::Tiny Set::Scalar Text::Table Exception::Class Test::Most Test::Warn Test::Exception Test::Deep Moose SVG Algorithm::Combinatorics

	sudo apt-get install mysql-server

	export DBD_MYSQL_LIBS="-L/usr/local/mysql/lib/mysql -lmysqlclient"
	export DBD_MYSQL_CONFIG=/etc/mysql/conf.d/mysql.cnf
	export DBD_MYSQL_NOCATCHSTDERR=0
	export DBD_MYSQL_NOFOUNDROWS=0
	export DBD_MYSQL_TESTHOST=localhost
	export DBD_MYSQL_TESTPASSWORD=ROOT PASSWORD
	export DBD_MYSQL_TESTUSER=root

	sudo apt install libmysqlclient-dev
	sudo apt-get install libdbd-mysql-perl
	cpan install DBD::mysql

	#STEP (2)
	#download and install the mcl program according to provided instructions.

	wget -P "$workingdir"/ https://www.micans.org/mcl/src/mcl-latest.tar.gz
	cd "$workingdir"/
	tar xzf mcl-latest.tar.gz
	cd mcl-*
	./configure
	make
	sudo make install
fi

#(3) install and configure the OrthoMCL suite of programs
if [ "$installorthomcl" = "yes" ]; then
	wget -P "$workingdir"/ http://orthomcl.org/common/downloads/software/v2.0/orthomclSoftware-v2.0.9.tar.gz
	cd "$workingdir"/
	tar xzf orthomclSoftware-v2.0.9.tar.gz
fi

#ORTHOMCL Pipeline

#create my_orthomcl working directories
mkdir "$orthodir"/../my_orthomcl_dir
mkdir "$orthodir"/../my_orthomcl_dir/compliantFasta
rm "$orthodir"/../my_orthomcl_dir/compliantFasta/*
rm -r pairs/
rm -r "$orthodir"/pairs/

#create MYSQL database
mysql -u root -p"$mysqlpass" -e "DROP DATABASE IF EXISTS orthomcl";
mysql -u root -p"$mysqlpass" -e "CREATE DATABASE IF NOT EXISTS orthomcl";

#create config file
rm "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "dbVendor=mysql" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "dbConnectString=dbi:mysql:orthomcl" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "dbLogin=root" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "dbPassword=$mysqlpass" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "similarSequencesTable=SimilarSequences" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "orthologTable=Ortholog" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "inParalogTable=InParalog" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "coOrthologTable=CoOrtholog" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "interTaxonMatchView=InterTaxonMatch" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "percentMatchCutoff=50" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "evalueExponentCutoff=-5" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config
echo "oracleIndexTblSpc=NONE" | tee -a "$orthodir"/../my_orthomcl_dir/orthomcl.config

#(4) run orthomclInstallSchema to install the required schema into the database
echo "========== Step 4: orthomclInstallSchema ========"
"$orthodir"/orthomclInstallSchema "$orthodir"/../my_orthomcl_dir/orthomcl.config "$orthodir"/../my_orthomcl_dir/install_schema.log

#(5) run orthomclAdjustFasta (or your own simple script) to generate protein fasta files in the required format
echo "=========== Step 5: orthomclAdjustFasta ========="
"$orthodir"/orthomclAdjustFasta "$taxon" "$fastainput" "$intlog"

#Copy Sugar.fas from orthomclAdjustFasta directory to /my_orthomcl_dir/compliantFasta/
cp "$taxon".fasta "$orthodir"/../my_orthomcl_dir/compliantFasta/

#(6) run orthomclFilterFasta to filter away poor quality proteins, and optionally remove alternative proteins.
echo "========== Step 6: orthomclFilterFasta =========="
"$orthodir"/orthomclFilterFasta "$orthodir"/../my_orthomcl_dir/compliantFasta/ 10 20 "$orthodir"/../my_orthomcl_dir/goodProteins.fas "$orthodir"/../my_orthomcl_dir/badProteins.fas

#(7) run all-v-all NCBI BLAST on goodProteins.fasta (output format is tab delimited text)
echo "============ Step 7: All-v-all BLAST ============"
if [ "$blastAVAfile" = "" ]; then
  makeblastdb -in "$orthodir"/../my_orthomcl_dir/compliantFasta/"$taxon".fasta -dbtype prot -out "$orthodir"/../my_orthomcl_dir/compliantFasta/"$taxon".fasta.blastdb
  blastp -query "$orthodir"/../my_orthomcl_dir/compliantFasta/"$taxon".fasta -db "$orthodir"/../my_orthomcl_dir/compliantFasta/"$taxon".fasta.blastdb -evalue 1e-5 -outfmt 6 -out "$orthodir"/../my_orthomcl_dir/all-vs-all.blastp
else
  rm "$orthodir"/../my_orthomcl_dir/all-vs-all.blastp
  cp "$blastAVAfile" "$orthodir"/../my_orthomcl_dir/all-vs-all.blastp
fi

#(8) run orthomclBlastParser on the NCBI BLAST tab output to create a file of similarities in the required format
echo "========== Step 8: orthomclBlastParser =========="
"$orthodir"/orthomclBlastParser "$orthodir"/../my_orthomcl_dir/all-vs-all.blastp "$orthodir"/../my_orthomcl_dir/compliantFasta/ > "$orthodir"/../my_orthomcl_dir/similarSequences.txt

#(9) run orthomclLoadBlast to load the output of orthomclBlastParser into the database
echo "=========== Step 9: orthomclLoadBlast  =========="
"$orthodir"/orthomclLoadBlast "$orthodir"/../my_orthomcl_dir/orthomcl.config "$orthodir"/../my_orthomcl_dir/similarSequences.txt

#(10) run the orthomclPairs program to compute pairwise relationships
echo "============ Step 10: orthomclPairs ============="
"$orthodir"/orthomclPairs "$orthodir"/../my_orthomcl_dir/orthomcl.config "$orthodir"/../my_orthomcl_dir/similarSequences.txt cleanup=no

#(11) run the orthomclDumpPairsFiles program to dump the pairs/ directory from the database
echo "======== Step 11: orthomclDumpPairsFiles ========"
#cp -r pairs/ "$orthodir"/
"$orthodir"/orthomclDumpPairsFiles "$orthodir"/../my_orthomcl_dir/orthomcl.config

#(12) run the mcl program on the mcl_input.txt file created in Step 11
echo "================= Step 12: mcl =================="
mcl mclInput --abc -I 1.5 -o "$orthodir"/../my_orthomcl_dir/mclOutput

#(13) run orthomclMclToGroups to convert mcl output to groups.txt
echo "========= Step 13: orthomclMclToGroups =========="
"$orthodir"/orthomclMclToGroups "$clusteracro" 1 < "$orthodir"/../my_orthomcl_dir/mclOutput > "$orthodir"/../my_orthomcl_dir/groups.txt
