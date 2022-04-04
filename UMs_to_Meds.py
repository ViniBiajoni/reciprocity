import numpy as np
import os
from gera_dados_caso import *
from crit_UMs import dfs
from printData import printCkUMs
import numpy as np
from itertools import combinations
import itertools


def obter_dicionario_listas(kmax):
    keys = list(range(kmax))
    dict_listas = {key: [] for key in keys}
    return dict_listas


#Gerar combinacoes de cardinalidades cruzadas
def gera_combinacoes_cardinalidade_cruzada(kmax, medidas_UMs, E):
    medidas_combnts = obter_dicionario_listas(kmax)
    #Todo - Implementar
    for i in range(kmax):
        lista_meds = medidas_UMs[i]
        for k in range(i, len(lista_meds)+1):
            for subset in combinations(lista_meds, k):
                medidas_combnts[k].append(set(subset))
    

#Gera combinacoes de mesma cardinalidade
def gera_combinacoes_mesma_cardinalidade(kmax, medidas_UMs, E): 
    medidas_combnts = obter_dicionario_listas(kmax)

    for i in range(kmax):
        lista_meds = medidas_UMs[i]
        kmax_meds = len(lista_meds) if (len(lista_meds) <= kmax + 1) else 5
        for k in range(i+1, kmax_meds + 1):
            for subset in itertools.combinations(lista_meds, k):
                medidas_combnts[i].append(set(subset))
    
    print('teste')


def recupera_ck_meds(kmax, num_cks, solution_list, dict_UMs_meds, E):
    #Monta dicionario de Medidas envolvidas (por cardinalidade)
    medidas_UMs = obter_dicionario_listas(kmax)

    for k in range(kmax):
        for ckUM in solution_list[k]:
            for i in range(k+1):
                medidas_UMs[k].append(dict_UMs_meds[f'{ckUM[i]}'])
        medidas_UMs[k] = list(set(itertools.chain.from_iterable(medidas_UMs[k])))

    combinacoes_medidas_k = gera_combinacoes_mesma_cardinalidade(kmax, medidas_UMs, E)
    print("teste")

if __name__ == "__main__":
    
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    num_bus = int(input("Digite o num de barras"))

    #Leitura Medicao

    #30 Bus
    # med_file= os.path.join(THIS_FOLDER,'ieee30_observability_PSCC_2014B_43.med')
    med_file= os.path.join(THIS_FOLDER,'24BusUM10eUM15.med')
    # med_file= os.path.join(THIS_FOLDER,'ieee24Case01_SBSE2014.med')
    # caso = 'ieee30_observability_PSCC_2014B_43'
    # caso = 'ieee24Case01_SBSE2014'
    caso = '24BusUM10eUM15'

    meds= np.loadtxt(med_file)
    num_meds = len(meds[:,0])

    #Leitura Sistema
    net_file= os.path.join(THIS_FOLDER,'sistemas\ieee24.txt')
    # net_file= os.path.join(THIS_FOLDER,'sistemas\ieee30.txt')
    net = np.loadtxt(net_file)

    #Monta H e esturura de relacoes entre medidas e UMs
    H,dict_meds,dict_UMs_meds,UMs = case_prepare(meds,net,num_bus,num_meds)

    #Monta G e E
    G =  np.transpose(H)@H
    E = np.identity(num_meds) - H@(np.linalg.inv(G))@np.transpose(H)

    #Call crit UMs analysis
    kmax = 3 
    solution_list, num_cks = dfs(E,num_meds,kmax,num_bus,UMs,dict_UMs_meds)
    printCkUMs(num_bus, num_meds, kmax, num_cks, solution_list)

    ck_meds_recuperadas = recupera_ck_meds(kmax, num_cks, solution_list, dict_UMs_meds, E)
    print("Finished")
##########################################Pós-processo análise Ck-meds######################################## 


    
   