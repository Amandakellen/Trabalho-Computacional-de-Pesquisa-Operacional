clear all
close all
clc

%Leitura dos Arquivos
equipamentos =csvread('EquipDB.csv');
plano_manutencao=csvread('MPDB.csv');
probabilidades = csvread('Probabilidade_de_falha.csv');


%Criando as variáveis
n_m = 500;%Quantidade de máquinas
m_p = 3;%Quantidade de planos de manutenção
Xij = binvar(n_m, m_p, 'full');%Matriz binária onde i são os equipamento e j são osos planos de manutenção
Pij = probabilidades(:,2:4);%Probabilidade de falha do equipamento i sob o planode manutenção j

%Variáveis auxiliares
Caux = equipamentos(:,4);%Variável auxiliar para salvar os dados dos custos de falha dos equipamentos
C = plano_manutencao(:,3);%Variável auxiliar para salvar os dados dos custos de aplicação do  plano  de  manutenção  do horizonte de planejamento 

%Salvando os custos em uma matriz de 500 linhas e 3 colunas para que assim
%se possa realizar a multiplicação termo a termo com a matriz Xij  e Pij nas
%funções objetivo

%CMJ=custos de aplicação do  plano  de  manutenção  do horizonte de planejamento 
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

%Criando as Restrições
restricoes =[] ;

for i = 1:n_m
        restricoes = [restricoes, (sum(Xij(i,:)))== 1];
end

%Gerando Matriz com pesos
iteracoes = 300;
pesos = [];
for i = 1:iteracoes
  aleatorio =  randi([1 20],1,2);
  %Condição criada para que os pesos w1() e w2 sejam diferentes entre si
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
%Calculando a solução ótima
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



