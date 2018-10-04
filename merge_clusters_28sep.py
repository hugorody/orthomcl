#!/usr/bin/python3

import clusterTHEMall_func

outDB = open("REFclustersDB_1oct2018.csv","w")

################################################################################
#COMPS INPUT FILES
orthocomp = "groups_comps.txt"
fastacomp = "../../references/Vicentinis/comps_plus_GGs.fas"
blastcomp = "all-vs-all_comps.blastp"
outcomp = "comps_allCLUSTERS.txt"

#DICTS
COMPStotalCLUSTERS = {} # {CLU1: "seq1,seq2,seq3..."}
COMPSseqsCLUSTERS = {} # {seq: CLU1, seq2: CLU1...}
################################################################################
#EVMS INPUT FILES
orthoevm = "groups_evms_fixed.txt"
fastaevm = "../../references/3280/Glaucias/sc.mlc.cns.sgl.utg.scga7.predicted_protein.fasta"
blastevm = "all-vs-all_evms_fixed.blastp"
outevm = "evms_allCLUSTERS.txt"

#DICTS
EVMStotalCLUSTERS = {} # {CLU1: "seq1,seq2,seq3..."}
EVMSseqsCLUSTERS = {} # {seq: CLU1, seq2: CLU1...}
################################################################################
#MONO
orthomono = "groups_mono.txt"
fastamono = "../../references/MonoploidReference/sugarcane_cds.fna"
blastmono = "all-vs-all_mono.blastp"
outmono = "mono_allCLUSTERS.txt"

#DICTS
MONOtotalCLUSTERS = {} # {CLU1: "seq1,seq2,seq3..."}
MONOseqsCLUSTERS = {} # {seq: CLU1, seq2: CLU1...}
################################################################################
#SORGO
orthosorgo = "groups_sorgo.txt"
fastasorgo = "../../references/Sorgo/Sbicolor_79_cds_primaryTranscriptOnly.fa"
blastsorgo = "all-vs-all_sorgo.blastp"
outsorgo = "sorgo_allCLUSTERS.txt"

#DICTS
SORGOtotalCLUSTERS = {} # {CLU1: "seq1,seq2,seq3..."}
SORGOseqsCLUSTERS = {} # {seq: CLU1, seq2: CLU1...}
################################################################################
#PRGDB
orthoprgdb = "groups_prgdb.txt"
fastaprgdb = "../../references/PRGDB/all_gene_reference.fa"
blastprgdb = "all-vs-all_prgdb.blastp"
outprgdb = "prgdb_allCLUSTERS.txt"

#DICTS
PRGDBtotalCLUSTERS = {} # {CLU1: "seq1,seq2,seq3..."}
PRGDBseqsCLUSTERS = {} # {seq: CLU1, seq2: CLU1...}
################################################################################
#Call the clusterTHEMall function
print (">> Clustering COMPs")
COMPS = clusterTHEMall_func.getCLU(orthocomp,fastacomp,blastcomp,outcomp,COMPStotalCLUSTERS,COMPSseqsCLUSTERS)

print ("\n>> Clustering MONO")
MONO = clusterTHEMall_func.getCLU(orthomono,fastamono,blastmono,outmono,MONOtotalCLUSTERS,MONOseqsCLUSTERS)

print ("\n>> Clustering SORGO")
SORGO = clusterTHEMall_func.getCLU(orthosorgo,fastasorgo,blastsorgo,outsorgo,SORGOtotalCLUSTERS,SORGOseqsCLUSTERS)

print ("\n>> Clustering PRGDB")
PRGDB = clusterTHEMall_func.getCLU(orthoprgdb,fastaprgdb,blastprgdb,outprgdb,PRGDBtotalCLUSTERS,PRGDBseqsCLUSTERS)

print ("\n>> Clustering EVMs")
EVMS = clusterTHEMall_func.getCLU(orthoevm,fastaevm,blastevm,outevm,EVMStotalCLUSTERS,EVMSseqsCLUSTERS)

################################################################################
comps_monoBH = {} # {comp: [best hit in mono, identity]}
comps_monoBLAST = "../../references/Vicentinis/comps_plus_GGs_vs_mono.blastn"
MONOBH = clusterTHEMall_func.besthit(comps_monoBLAST,comps_monoBH)

comps_sorgoBH = {} # {comp: [best hit in sorgo, identity]}
comps_sorgoBLAST = "../../references/Vicentinis/comps_plus_GGs_vs_sorgo_fixed.blastx"
SORGOBH = clusterTHEMall_func.besthit(comps_sorgoBLAST,comps_sorgoBH)

comps_prgdbBH = {} # {comp: [best hit in prgdb, identity]}
comps_prgdbBLAST = "../../references/Vicentinis/comps_plus_GGs_vs_prgdb.blastx"
PRGDB = clusterTHEMall_func.besthit(comps_prgdbBLAST,comps_prgdbBH)

comps_evmsBH = {} # {comp: [best hit in evms, identity]}
comps_evmsBLAST = "/home/hugo/Documents/orthomcl/backup/comps_plust_ggs_vs_evms.blast"
EVMBH = clusterTHEMall_func.besthit(comps_evmsBLAST,comps_evmsBH)

################################################################################
#Getting final clusters
#COMP vs MONO
cluster_compmono = {} # {SIN73071: ['Sh_220I13_t000080', '99.630', 'CLU4308', 'gg_16154']}
getcompmono = clusterTHEMall_func.finalcluster(COMPStotalCLUSTERS,MONOseqsCLUSTERS,MONOtotalCLUSTERS,comps_monoBH,cluster_compmono)

#COMP vs SORGO
cluster_compsorgo = {} # {SIN73071: ['Sh_220I13_t000080', '99.630', 'CLU4308', 'gg_16154']}
getcompsorgo = clusterTHEMall_func.finalcluster(COMPStotalCLUSTERS,SORGOseqsCLUSTERS,SORGOtotalCLUSTERS,comps_sorgoBH,cluster_compsorgo)

#COMP vs PRGDB
cluster_compprgdb = {} # {SIN73071: ['Sh_220I13_t000080', '99.630', 'CLU4308', 'gg_16154']}
getprgdb = clusterTHEMall_func.finalcluster(COMPStotalCLUSTERS,PRGDBseqsCLUSTERS,PRGDBtotalCLUSTERS,comps_prgdbBH,cluster_compprgdb)

#COMP vs EVM
cluster_compevm = {} # {SIN73071: ['Sh_220I13_t000080', '99.630', 'CLU4308', 'gg_16154']}
getevm = clusterTHEMall_func.finalcluster(COMPStotalCLUSTERS,EVMSseqsCLUSTERS,EVMStotalCLUSTERS,comps_evmsBH,cluster_compevm)

################################################################################

for i in COMPStotalCLUSTERS.items():
    line = []
    line.append(cluster_compmono[i[0]][3] + " " + " ".join(cluster_compmono[i[0]][0:3]) + " " + cluster_compmono[i[0]][4])
    line.append(cluster_compsorgo[i[0]][3] + " " + " ".join(cluster_compsorgo[i[0]][0:3]) + " " + cluster_compsorgo[i[0]][4])
    line.append(cluster_compprgdb[i[0]][3] + " " + " ".join(cluster_compprgdb[i[0]][0:3]) + " " + cluster_compprgdb[i[0]][4])
    line.append(cluster_compevm[i[0]][3] + " " + " ".join(cluster_compevm[i[0]][0:3]) + " " + cluster_compevm[i[0]][4])

    outDB.write(i[0] + " " + i[1] + " " + str(len(i[1].split(","))) + " " + " ".join(line) + "\n")
