import csv

#Abrindo arquivos   CSV
arquivo_cluster=open('ClusterDB.csv')
arquivo_manutencao=open('MPDB.csv')
arquivo_maquinas=open('EquipDB.csv')

#Leitura dos arquivos
cluster=csv.reader(arquivo_cluster)
manutencao=csv.reader(arquivo_manutencao)
maquinas=csv.reader(arquivo_maquinas)

linha=0
coluna=0

#Inicializando as Matrizes
matriz_cluster = [ [0 for i in range(3)] for j in range(4)]
matriz_manutencao=[ [0 for i in range(3)] for j in range(3)]
matriz_maquinas=[ [0 for i in range(4)] for j in range(500)]
matriz_confiabilidade=

#Salvando os dados dos csvs em uma matriz
for row in cluster:
    coluna=0
    while coluna!=3:
        matriz_cluster[linha][coluna] = float(row[coluna])
        coluna=coluna+1
    linha=linha+1

linha=0
coluna=0

for i in manutencao:
    coluna = 0
    while coluna != 3:
        matriz_manutencao[linha][coluna] = float(i[coluna])
        coluna = coluna + 1
    linha = linha + 1

linha=0
coluna=0

for i in maquinas:
    coluna = 0
    while coluna != 4:
        matriz_maquinas[linha][coluna] = float(i[coluna])
        coluna = coluna + 1
    linha = linha + 1



#Fechando arquivos
arquivo_cluster.close()
arquivo_manutencao.close()
arquivo_maquinas.close()