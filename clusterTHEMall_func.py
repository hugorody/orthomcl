#!/usr/bin/python3

# file1 = orthomcl file
# file2 = fasta file
# file3 = blast all vs all of species
# out1 = name to write the output
def getCLU(file1,file2,file3,out1,totalDICT,seqsDICT):

    with open(file1,"r") as set1:
        for i in set1:
            i = i.rstrip().replace("Taxon1|","").replace(":","")
            i = i.split(" ")
            totalDICT[i[0]] = ",".join(i[1:])
            for j in range(1,len(i)):
                seqsDICT[i[j]] = i[0]

    print ("Number of genes in OrthoMCL clusters",len(seqsDICT))

    #read fasta file and verify which of gene IDs are not forming clustersorthomclfile
    tmpsingles = {}
    with open(file2,"r") as set2:
        for i in set2:
            i = i.rstrip()
            if ">" in i:
                gene = i.replace(">","").split(" ")[0]
                if gene not in seqsDICT:
                    tmpsingles[gene] = ''

    #read all-vs-all blast file and check if the gene IDS from temporary single genes
    #have identity >40 to other sequences and form temporary new clusters
    blacklist = {}
    tmpclus = {} # {comp1: [comp2,comp3...],n...}
    with open(file3,"r") as set3:
        for i in set3:
            i = i.rstrip().replace("Taxon1|","")
            i = i.split("\t")
            if i[0] != i[1] and float(i[2]) >= 40:
                if i[0] in tmpsingles and i[1] in tmpsingles and i[0] not in blacklist and i[1] not in blacklist:
                    blacklist[i[1]] = ''
                    if i[0] not in tmpclus:
                        tmpclus[i[0]] = [i[1]]
                    else:
                        addpar = tmpclus[i[0]]
                        addpar.append(i[1])
                        tmpclus[i[0]] = addpar

    #create the new clusters for compsGGs sequences
    #based on the temporary clusters, create the new clusters with index starting from
    #the size of comps clusters predicted by orthomcl
    #also, update dict totalDICT with the new clusters
    clucount = len(totalDICT) + 1
    compidentclusters = {} #{comp1: CLU1, comp2: CLU1, n...}
    for i in tmpclus.items():
        #update totalDICT
        addclu = i[1]
        addclu.append(i[0])
        totalDICT["NCLU"+str(clucount)] = ",".join(addclu)

        if i[0] not in seqsDICT:
            seqsDICT[i[0]] = "NCLU"+str(clucount)

        for j in i[1]:
            if j not in seqsDICT:
                seqsDICT[j] = "NCLU"+str(clucount)
        clucount += 1

    realsingles = {}
    for i in tmpsingles.keys():
        if i not in compidentclusters:
            if i not in seqsDICT:
                realsingles[i] = ''
                totalDICT["SIN"+str(clucount)] = i
                seqsDICT[i] = "SIN"+str(clucount)
                clucount += 1

    clustersoutput = open(out1,"w")
    #calculate maximum clusters size
    maxclusize = 0
    for i in totalDICT.items():
        clustersoutput.write(i[0] + ":" + "\t" + i[1] + "\n")
        sizeclu = len(i[1].split(","))
        if sizeclu > maxclusize:
            maxclusize = sizeclu

    print ("Total number of genes with OrthoMCL and New clusters",len(seqsDICT))
    print ("Total number of clusters:",len(totalDICT))
    print ("Max cluster size:",maxclusize)

def besthit(inputfile,dictBestHit):
    print ("Best Hit for",inputfile)
    with open(inputfile,"r") as set1:
        for i in set1:
            i = i.rstrip()
            i = i.split("\t")
            if i[0] != i[1]:
                if i[0] not in dictBestHit:
                    dictBestHit[i[0]] = [i[1],i[2]]
                else:
                    if float(i[2]) > float(dictBestHit[i[0]][1]):
                        dictBestHit[i[0]] = [i[1],i[2]]

def finalcluster(totalCOMP,seq_cluster,total_cluster,comps_BH,cluster):
    for i in totalCOMP.items():
        for j in i[1].split(","):
            if j in comps_BH:
                if i[0] not in cluster:
                    vals = comps_BH[j]
                    vals.append(seq_cluster[comps_BH[j][0]])
                    vals.append(j)
                    vals.append(str(len(total_cluster[vals[2]].split(","))))
                    cluster[i[0]] = vals
                    #print (i[0],vals)
                else:
                    if float(cluster[i[0]][1]) > float(comps_BH[j][1]):
                        vals = comps_BH[j]
                        vals.append(seq_cluster[comps_BH[j][0]])
                        vals.append(j)
                        vals.append(str(len(total_cluster[vals[2]].split(","))))
                        cluster[i[0]] = vals
            else:
                cluster[i[0]] = ["NaN","0","NaN","NaN","NaN"]
