import csv

#Abrindo arquivos   CSV
arquivo_cluster=open('ClusterDB.csv')
arquivo_manutencao=open('MPDB.csv')

cluster=csv.reader(arquivo_cluster)
manutencao=csv.reader(arquivo_manutencao)

linha=0
coluna=0
matrizcluster = [ [0 for i in range(3)] for j in range(4)]
for row in cluster:
    coluna=0
    while coluna!=3:
        matrizcluster[linha][coluna] = float(row[coluna])
        coluna=coluna+1
    linha=linha+1

#Fechando arquivos
arquivo_cluster.close()
arquivo_manutencao.close()
