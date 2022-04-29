from asyncio.windows_events import NULL
import numpy as np
import os
from gera_dados_caso import *
from crit_UMs import dfs
from printData import printCkUMs
import numpy as np
from crit_meds import meas_criticalities
from deepdiff import DeepDiff 
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
def gera_combinacoes_cardinalidade_cruzada(kmax_UM, kmax_med, medidas_UMs, E):
    medidas_combnts = obter_dicionario_listas(kmax_med)
    list_avaliados = list(())
    for i in range(kmax_UM - 1):
        lista_meds =  list(medidas_UMs[i])
        if i ==0:
            for subset in itertools.combinations(lista_meds, 1):           
                is_crit = avaliar_candidato(subset, E)
                if is_crit == True: 
                    medidas_combnts[0].append(set(subset))
        for j in range(i+1, kmax_UM):
            lista_meds2 = list(medidas_UMs[j]) 
            lista_completa = set(lista_meds + lista_meds2)
            for k in range(i+2, kmax_med+1):
                for subset in itertools.combinations(lista_completa, k):           
                    is_crit = avaliar_candidato(subset, E)
                    if is_crit == True: 
                        if subset not in list_avaliados:
                            list_avaliados.append(subset) 
                            medidas_combnts[k-1].append(set(subset))
    return medidas_combnts 
    

#Gera combinacoes de mesma cardinalidade
def gera_combinacoes_mesma_cardinalidade(kmax_UM,kmax_med, medidas_UMs, E): 
    if kmax_UM < kmax_med:
        kmax_med = kmax_UM
    medidas_combnts = obter_dicionario_listas(kmax_med)
    list_avaliados = list(()) 
    for i in range(kmax_med): 
        lista_meds = medidas_UMs[i]
        for k in range(i+1, kmax_med + 1):
            for subset in itertools.combinations(lista_meds, k):             
                is_crit = avaliar_candidato(subset, E)
                if is_crit == True: 
                    if subset not in list_avaliados:
                        list_avaliados.append(subset) 
                        medidas_combnts[k-1].append(set(subset))
    return medidas_combnts  
    

def recuperar_ck_meds(kmax_UM, kmax_med, num_cks, solution_list, dict_UMs_meds, E): #saida esperada -> Dicionario por cadinalidade com cks (Identico ao das UMs)
    #Monta dicionario de Medidas envolvidas (por cardinalidade)
    medidas_UMs = obter_dicionario_listas(kmax_UM)
    for k in range(kmax_UM):
        for ckUM in solution_list[k]:
            for i in range(k+1):
                medidas_UMs[k].append(dict_UMs_meds[f'{ckUM[i]}'])
        medidas_UMs[k] = list(set(itertools.chain.from_iterable(medidas_UMs[k])))
    combinacoes_medidas_k = gera_combinacoes_mesma_cardinalidade(kmax_UM, kmax_med, medidas_UMs, E)
    combinacoes_medidas_cruzadas_k = gera_combinacoes_cardinalidade_cruzada(kmax_UM, kmax_med, medidas_UMs, E)
    return combinacoes_medidas_k, combinacoes_medidas_cruzadas_k


def recuperar_ck_meds(kmax_UM, kmax_med, num_cks, solution_list, dict_UMs_meds, E): #saida esperada -> Dicionario por cadinalidade com cks (Identico ao das UMs)
    #Monta dicionario de Medidas envolvidas (por cardinalidade)
    medidas_UMs = obter_dicionario_listas(kmax_UM)
    for k in range(kmax_UM):
        for ckUM in solution_list[k]:
            for i in range(k+1):
                medidas_UMs[k].append(dict_UMs_meds[f'{ckUM[i]}'])
        medidas_UMs[k] = list(set(itertools.chain.from_iterable(medidas_UMs[k])))
    combinacoes_medidas_k = gera_combinacoes_mesma_cardinalidade(kmax_UM, kmax_med, medidas_UMs, E)
    combinacoes_medidas_cruzadas_k = gera_combinacoes_cardinalidade_cruzada(kmax_UM, kmax_med, medidas_UMs, E)
    return combinacoes_medidas_k, combinacoes_medidas_cruzadas_k


def filtra_ck_meds(kmax, dct_ck_med):
    for i in range(len(dct_ck_med)):
        for ckmed in dct_ck_med[i]:
            for k in range (i+1, len(dct_ck_med)):
                aux_list = list(dct_ck_med[k])
                for ckmed2 in aux_list:
                    if set(ckmed).issubset(set(ckmed2)):
                        dct_ck_med[k].remove(ckmed2)
    return dct_ck_med


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
    kmax_UM = 3
    kmax_med = 3  
    #todo - separar em kmax_UM e kmax_med
    solution_list, num_cks = dfs(E,num_meds,kmax_UM,num_bus,UMs,dict_UMs_meds)
    printCkUMs(num_bus, num_meds, kmax_UM, num_cks, solution_list)

    # Recuperar
    #recuperar medidas dentro da mesma criticalidade (de UM)
    dicionario_ck_meds_recuperadas1, dicionario_ck_meds_recuperadas2= recuperar_ck_meds(kmax_UM, kmax_med, num_cks, solution_list, dict_UMs_meds, E)


    #Filtrar
    # Percorrer o dionario de cks e remover aquelas que estão contidas em alguma de cardinalidade superior (Cj c Ck onde j<k)
    filtra_ck_meds(kmax_med, dicionario_ck_meds_recuperadas1)
    filtra_ck_meds(kmax_med, dicionario_ck_meds_recuperadas2)



    # Obtem criticalidades medidas via BF
    number_of_cks_meds, dicionario_ckMeds, _ = meas_criticalities(E,num_meds,kmax_med,num_bus,0,dict_meds)
    

    ##########################################Pós-processo análise Ck-meds######################################## 
    
    #Compara as criticalidades recuperadas via heurística com as completas
        #Todo - Implementar metodo compararativo
    
ddiff = DeepDiff(dicionario_ck_meds_recuperadas1, dicionario_ckMeds, ignore_order=True, view = 'tree')
print (ddiff)   


    
    #Printar as cks recuperadas por cardinalidade
    
with open('ckUMs_to_ckmeds'+f'{num_bus}bus' + f'_{num_meds}meds_'+ 'complete' + '.txt', 'w') as f:
        f.write(f'====Measurements Criticality Analysis From Measurement Units Analysis - Complete=====\n')
        f.write(f'kmax_UM = {kmax_UM}\n')
        f.write(f'kmax_med = {kmax_med}\n')
        #f.write(f'exec time = {toc - tic} seconds')
        f.write('\n \n')
        if kmax_UM < kmax_med:
            kmax = kmax_UM
        else:
            kmax = kmax_med
        for k in range(kmax):
            f.write(f'======================================c{k+1}-Tuples======================================\n')
            f.write(f'num ck-tuples = {len(dicionario_ckMeds[k])}\n\n')
            for elem in dicionario_ckMeds[k]:
                ck = list(elem)
                for i in range(len(ck)):
                    f.write('[%s]'% (ck[i]))
                f.write('\n')
            f.write('\n\n')
            f.write(f'num recovered ck-tuples = {len(dicionario_ck_meds_recuperadas1[k])}\n\n')
            for elem in dicionario_ck_meds_recuperadas1[k]:
                ck = list(elem)
                for i in range(len(ck)):
                    f.write('[%s]'% (ck[i]))
                f.write('\n') 
        f.close()  
        
with open('ckUMs_to_ckmeds'+f'{num_bus}bus' + f'_{num_meds}meds_' + 'summary' + '.txt', 'w') as f:
        f.write(f'=====Measurements Criticality Analysis From Measurement Units Analysis - Summary=====\n')
        f.write(f'kmax_UM = {kmax_UM}\n')
        f.write(f'kmax_med = {kmax_med}\n')
        #f.write(f'exec time = {toc - tic} seconds')
        f.write('\n \n')
        for k in range(kmax_med):
            f.write(f'======================================c{k+1}-Tuples======================================\n')
            f.write(f'num ck-tuples = {len(dicionario_ckMeds[k])}\n\n')
            f.write(f'num recovered ck-tuples = {len(dicionario_ck_meds_recuperadas2[k])}\n\n')
        f.write(f'====================================ck-Tuples Missing====================================\n')
        for tp in ddiff['iterable_item_added']:
            f.write(f'{tp.t2}\n')
        f.close() 
        
print("FIM DO PROGRAMA")



    
   