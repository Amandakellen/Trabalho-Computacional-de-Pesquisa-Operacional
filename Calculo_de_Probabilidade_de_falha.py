import csv
from math import *
import pandas as pd

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
matriz_confiabilidade=[ [0 for i in range(4)] for j in range(500)]#1º coluna id da máquina e 2º coluna a probabilidade de falha do plano de manutenção1
#3º coluna a probabilidade de falha do plano de manutenção 2 e 4ºcoluna a probabilidade de falha do plano de manutenção 3

#Variaveis auxiliares
#1º coluna id da máquina e 2º coluna a probabilidade de falha do plano de manutenção1
#3º coluna a probabilidade de falha do plano de manutenção 2 e 4ºcoluna a probabilidade de falha do plano de manutenção 3
matriz_ft0=[ [0 for i in range(2)] for j in range(500)]
matriz_fk=[ [0 for i in range(4)]for j in range(500)]

deltat=5 #em anos

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


#Calculo probabilidade de Falha T0

for i in range(500):
    j = 0
    matriz_ft0[i][0]=i+1

    #Verificar o Cluster que a maquina pertence
    if matriz_maquinas[i][2]==1.0:
        beta=matriz_cluster[0][2]
        eta=matriz_cluster[0][1]
    elif matriz_maquinas[i][2]==2.0:
        beta = matriz_cluster[1][2]
        eta = matriz_cluster[1][1]
    elif matriz_maquinas[i][2] ==3.0:
        beta = matriz_cluster[2][2]
        eta = matriz_cluster[2][1]
    elif matriz_maquinas[i][2] ==4.0:
        beta = matriz_cluster[3][2]
        eta = matriz_cluster[3][1]

    t0=matriz_maquinas[i][1]
    aux1=t0/eta
    aux1=aux1**beta
    aux2=1-exp(-aux1)

    matriz_ft0[i][1]=1-exp(-((t0/eta)**beta))

#Calculo probabilidade de Falha Tk
for i in range(500):
    matriz_fk[i][0]=i+1

    #Verificar o Cluster que a maquina pertence
    if matriz_maquinas[i][2]==1.0:
        beta=matriz_cluster[0][2]
        eta=matriz_cluster[0][1]
    elif matriz_maquinas[i][2]==2.0:
        beta = matriz_cluster[1][2]
        eta = matriz_cluster[1][1]
    elif matriz_maquinas[i][2] ==3.0:
        beta = matriz_cluster[2][2]
        eta = matriz_cluster[2][1]
    elif matriz_maquinas[i][2] ==4.0:
        beta = matriz_cluster[3][2]
        eta = matriz_cluster[3][1]

    t0=matriz_maquinas[i][1]

    #Plano de  manutenção 1
    matriz_fk[i][1]=1-exp(-(((t0+(matriz_manutencao[0][1]*deltat))/eta)**beta))

    #Plano de manutenção 2
    matriz_fk[i][2]=1-exp(-(((t0+(matriz_manutencao[1][1]*deltat))/eta)**beta))

    #Plano de Manutenção 3
    matriz_fk[i][3]=1-exp(-(((t0+(matriz_manutencao[2][1]*deltat))/eta)**beta))


#Calculando a probabilidade de falha de cada máquina em cada plano de manutenção
for i in range(500):
    matriz_confiabilidade[i][0]=i+1

    #Plano de manutenção 1
    matriz_confiabilidade[i][1]=((matriz_fk[i][1]-matriz_ft0[i][1])/(1-matriz_ft0[i][1]))

    #Plano de Manutenção 2
    matriz_confiabilidade[i][2] = ((matriz_fk[i][2] - matriz_ft0[i][1]) / (1 - matriz_ft0[i][1]))

    # Plano de Manutenção 2
    matriz_confiabilidade[i][3] = ((matriz_fk[i][3] - matriz_ft0[i][1]) / (1 - matriz_ft0[i][1]))

#Salvando a matriz em um arquivo csv
pd.DataFrame(matriz_confiabilidade).to_csv("Probabilidade_de_falha.csv",header=None, index=None)

#Fechando arquivos

arquivo_cluster.close()
arquivo_manutencao.close()
arquivo_maquinas.close()