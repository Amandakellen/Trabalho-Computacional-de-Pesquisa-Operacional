clear all
close all
clc

%Leitura dos Arquivos
equipamentos =csvread('EquipDB.csv');
plano_manutencao=csvread('MPDB.csv');
probabilidades = csvread('Probabilidade_de_falha.csv');


%Criando as vari�veis
n_m = 500;%Quantidade de m�quinas
m_p = 3;%Quantidade de planos de manuten��o
Xij = binvar(n_m, m_p, 'full');%Matriz bin�ria onde i s�o os equipamento e j s�o osos planos de manuten��o
Pij = probabilidades(:,2:4);%Probabilidade de falha do equipamento i sob o planode manuten��o j

%Vari�veis auxiliares
Caux = equipamentos(:,4);%Vari�vel auxiliar para salvar os dados dos custos de falha dos equipamentos
C = plano_manutencao(:,3);%Vari�vel auxiliar para salvar os dados dos custos de aplica��o do  plano  de  manuten��o  do horizonte de planejamento 

%Salvando os custos em uma matriz de 500 linhas e 3 colunas para que assim
%se possa realizar a multiplica��o termo a termo com a matriz Xij  e Pij nas
%fun��es objetivo

%CMJ=custos de aplica��o do  plano  de  manuten��o  do horizonte de planejamento 
Cmj=[]
for i=1:n_m
    for j=1:m_p
      Cmj(i,j)= C(j,1)
    end
end

%Ci=custos de falha dos equipamentos
Ci=[]
for i=1:n_m
    for j=1:m_p
      Ci(i,j)= Caux(i,1)
    end
end

%Criando as Restri��es
restricoes =[] ;

for i = 1:n_m
        restricoes = [restricoes, (sum(Xij(i,:)))== 1];
end

%Gerando Matriz com pesos
iteracoes = 300;
pesos = [];
for i = 1:iteracoes
  aleatorio =  randi([1 20],1,2);
  %Condi��o criada para que os pesos w1() e w2 sejam diferentes entre si
  %sendo w1=pesos(i,1) e w2=pesos(i,2)
  if aleatorio(1,1)==aleatorio(1,2)
    while aleatorio(1,1)==aleatorio(1,2)
        aleatorio =  randi([1 10],1,2);
    end
    pesos(i,1)=aleatorio(1,1);
    pesos(i,2)=aleatorio(1,2);
  else
      pesos(i,1)=aleatorio(1,1);
      pesos(i,2)=aleatorio(1,2);
  end
    
end    


%Objetivo
%Calculando a solu��o �tima
Resultados=[];
for i =1:iteracoes
  Objetivo = pesos(i,1) * sum(sum(Cmj.*Xij)) + pesos(i,2) * sum(sum(Ci.*Xij.*Pij));
  Opcoes = sdpsettings('solver', 'gurobi');
  solucao = optimize(restricoes,Objetivo,Opcoes);
  otima=value(Xij);
  for j=1:n_m
      if otima(j,1)==1
          Resultados(i,j)=1;
      end
      if otima(j,2)==1
         Resultados(i,j)=2;
      end
      if otima(j,3)==1
          Resultados(i,j)=3;
      end
  
  end
  
end
writematrix(Resultados, "AmandaPinho.csv")



