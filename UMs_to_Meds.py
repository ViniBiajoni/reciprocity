import numpy as np
import os
from gera_dados_caso import *
from crit_UMs import dfs
from printData import printCkUMs
import numpy as np
from itertools import combinations
from crit_meds import meas_criticalities
import itertools
import scipy



def avaliar_candidato(meas_envolved,E):
    n_meas = len(list(meas_envolved))
    E_aux = np.zeros((n_meas,n_meas))
    
    for i in range(n_meas):
        E_aux[i,i] = E[meas_envolved[i],meas_envolved[i]]
        for j in range(i+1,n_meas):
            E_aux[i,j] = E[meas_envolved[i],meas_envolved[j]]
            E_aux[j,i] = E_aux[i,j]

    P, L, U = scipy.linalg.lu(E_aux)

    is_crit = False

    if min(abs(np.diag(U))) < 1e-10:
        is_crit = True
    
    return is_crit

def obter_dicionario_listas(kmax):
    keys = list(range(kmax))
    dict_listas = {key: [] for key in keys}
    return dict_listas


#Gerar combinacoes de cardinalidades cruzadas
def gera_combinacoes_cardinalidade_cruzada(kmax, medidas_UMs, E):
    medidas_combnts = obter_dicionario_listas(kmax)
    #Todo - Implementar
    

#Gera combinacoes de mesma cardinalidade
def gera_combinacoes_mesma_cardinalidade(kmax, medidas_UMs, E): 
    medidas_combnts = obter_dicionario_listas(kmax)
    
    for i in range(kmax): #(kmin com ck, kmax)
        lista_meds = medidas_UMs[i]
        kmax_meds = len(medidas_UMs) if (len(medidas_UMs) <= kmax + 1) else 5
        for k in range(i+1, kmax_meds + 1):
            for subset in itertools.combinations(lista_meds, k):             
                is_crit = avaliar_candidato(subset, E)
                if is_crit == True: 
                    medidas_combnts[k -1].append(set(subset))
    return medidas_combnts  
    

def recuperar_ck_meds(kmax, num_cks, solution_list, dict_UMs_meds, E): #saida esperada -> Dicionario por cadinalidade com cks (Identico ao das UMs)
    #Monta dicionario de Medidas envolvidas (por cardinalidade)
    medidas_UMs = obter_dicionario_listas(kmax)

    for k in range(kmax):
        for ckUM in solution_list[k]:
            for i in range(k+1):
                medidas_UMs[k].append(dict_UMs_meds[f'{ckUM[i]}'])
        medidas_UMs[k] = list(set(itertools.chain.from_iterable(medidas_UMs[k])))
    combinacoes_medidas_k = gera_combinacoes_mesma_cardinalidade(kmax, medidas_UMs, E)
    return combinacoes_medidas_k

if __name__ == "__main__":
    
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    #num_bus = int(input("Digite o num de barras"))
    num_bus = 24
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

    # Recuperar
    dicionario_ck_meds_recuperadas = recuperar_ck_meds(kmax, num_cks, solution_list, dict_UMs_meds, E)

    # dicionario_ck_meds_recuperadas1 = recuperar_ck_meds_combinacao_interna(kmax, num_cks, solution_list, dict_UMs_meds, E)
    # dicionario_ck_meds_recuperadas2 = recuperar_ck_meds_combinacao_cruzada(kmax, num_cks, solution_list, dict_UMs_meds, E)



    #Filtrar
        #Todo - Implementar Método de filtragem
            # Percorrer o dionario de cks e remover aquelas que estão contidas em alguma de cardinalidade superior (Cj c Ck onde j<k)



    # Obtem criticalidades medidas via BF
    number_of_cks_meds, dicionario_ckMeds, _ = meas_criticalities(E,num_meds,kmax,num_bus,0,dict_meds)
    
    
    ##########################################Pós-processo análise Ck-meds######################################## 
    
    #Compara as criticalidades recuperadas via heurística com as completas
        #Todo - Implementar metodo compararativo

    teste = True
    
    
    #Printar as cks recuperadas por cardinalidade
    
    



    
   