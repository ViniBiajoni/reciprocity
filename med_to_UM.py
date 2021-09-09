import numpy as np
import pandas as pd
import subprocess
import os
import itertools

from collections import Counter

def checkInFirst(a, b):
     #getting count
    count_a = Counter(a)
    count_b = Counter(b)
  
    #checking if element exsists in second list
    for key in count_b:
        if key not in  count_a:
            return False
        if count_b[key] > count_b[key]:
            return False
    return True

#Leitura da Matriz de Covar
nbar = 30
nmed = 43
kmax = 6
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
E_file = os.path.join(THIS_FOLDER,"E_30bus43m.txt")
E = np.loadtxt(E_file)


#Leitura do Arquivo de Medidas
medicao= os.path.join(THIS_FOLDER,'ieee30_observability_PSCC_2014B_43.med')
medidas= np.loadtxt(medicao)

#Criar Vetor Med->UM
med_to_um = medidas[:,5]
med_to_um = [ int(elem) for elem in med_to_um]

#Prepara e Executa Analise de Crits Medidas em C
nrows= int(nmed)
ncols= int(nmed)
vector = np.reshape(E, (1, nrows*ncols))
f = open("E_teste.txt", "w+")
f.write("%d " % (int(nbar)))
f.write("%d " % (int(nmed)))
f.write("%d\n" % (int(kmax)))
for m in range(nrows):
    for n in range(ncols):
        f.write("%1.15f " % (vector[0,m*ncols + n]))
    f.write("\n")
f.close() 

##########################################Pós-processo análise Ck-meds######################################## 
if os.path.exists("Crits.csv"):
  os.remove("Crits.csv") 
else:
  print("The file does not exist yet")

subprocess.Popen([r"CritsFind_complete.exe"])

finished = False
while finished == False:
    if os.path.exists("Crits.csv"):
        break
    # else:
        # print("The file does not exist yet")
# time.sleep(1)
file_crits= 'Crits.csv'
colNames=['Criticalidades']
crits =  pd.read_csv(file_crits,names=colNames)
j=0
card = []
integer_list = []
############################Monta Dicionario por Cardinalidade c/ as Criticalidades de Medidas########################################
for c in crits['Criticalidades']:
    temp=c.split()
    integer_map = map(int, temp)
    integer_list.append(list(integer_map))
    card.append(len(integer_list[j]))
    j=j+1
    card_max= max(card)

keys = list(range(kmax))
sol_list_med_number = {key: [] for key in keys}
for ck in integer_list:
    tupla=[]
    for i in ck:
        tupla.append(i)
    sol_list_med_number[len(ck)-1].append(set(tupla))
    
#############################Number of Criticalities per Cardinality################
number_of_cks_meds = [card.count(i+1) for i in range(card_max)]

##############################Obtencao das CK-UMs###################################
ck_meds=[]
for i in range(kmax):
    ck_meds.append(sol_list_med_number[i])
ck_meds = list(itertools.chain.from_iterable(ck_meds))

ck_UMs_candidates=[]
for i in ck_meds:
    temp=[]
    for elements in list(i):
        temp.append(med_to_um[int(elements)])
    ck_UMs_candidates.append(set(temp))

n_candidatas =len(ck_UMs_candidates)
confirmadas = [1]*n_candidatas

for i in range(n_candidatas):
    for j in range(n_candidatas):
        if(ck_UMs_candidates[i].issubset(ck_UMs_candidates[j]) and ck_UMs_candidates[i]!= ck_UMs_candidates[j]):  confirmadas[j]=0

cont=0
for i in range(n_candidatas):
    if confirmadas[i] != 0:
        print(f'[{ck_UMs_candidates[i]}]')
        print('\n')
        if len(ck_UMs_candidates[i]) <= 3:
            cont+=1
        
print("ACABOOOOU")