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
    list_criticos = list(())
    count_checks = 0
    for i in range(kmax_UM - 1):
        lista_meds =  list(medidas_UMs[i])
        if i ==0:
            for subset in itertools.combinations(lista_meds, 1):           
                is_crit = avaliar_candidato(subset, E)
                if is_crit == True: 
                    medidas_combnts[0].append(set(subset))
                    list_criticos.append(subset) 
        for j in range(i+1, kmax_UM):
            lista_meds2 = list(medidas_UMs[j]) 
            lista_completa = set(lista_meds + lista_meds2)
            for k in range(i+2, kmax_med+1):
                for subset in itertools.combinations(lista_completa, k):           
                    if subset not in list_criticos:     
                        if checa_ck_med(subset, list_criticos):
                            count_checks += 1
                            is_crit = avaliar_candidato(subset, E)
                            if is_crit == True: 
                                if subset not in list_criticos:
                                    list_criticos.append(subset) 
                                    medidas_combnts[k-1].append(set(subset))
    return medidas_combnts, count_checks 
    

#Gera combinacoes de mesma cardinalidade
def gera_combinacoes_mesma_cardinalidade(kmax_UM,kmax_med, medidas_UMs, E): 
    medidas_combnts = obter_dicionario_listas(kmax_med)
    list_criticos = list(())
    count_checks = 0 
    for i in range(kmax_UM): 
        lista_meds = medidas_UMs[i]
        for k in range(i+1, kmax_med + 1):
            for subset in itertools.combinations(lista_meds, k):
                if subset not in list_criticos:
                    count_checks += 1
                    if checa_ck_med(subset, list_criticos):             
                        is_crit = avaliar_candidato(subset, E)
                        if is_crit == True: 
                            list_criticos.append(subset) 
                            medidas_combnts[k-1].append(set(subset))
    return medidas_combnts, count_checks  


#Gera combinacoes de mesma cardinalidade com inteligencia 
def gera_combinacoes_inteligentes(kmax_UM,kmax_med, medidas_UMs, E): 
    medidas_combnts = obter_dicionario_listas(kmax_med)
    list_criticos = list(())
    count_checks = 0
    #para criticalidades de cardinalidade 1, usamos a tecnica da combinação na mesma cardinalidade
    for x in range(1, kmax_med+1):
        for subset in itertools.combinations(medidas_UMs[0], x):
            if subset not in list_criticos:
                if checa_ck_med(subset, list_criticos):
                    count_checks += 1             
                    is_crit = avaliar_candidato(subset, E)
                    if is_crit == True: 
                        list_criticos.append(subset) 
                        medidas_combnts[x-1].append(set(subset))
    #para outras cardinalidades usamos a tecnica inteligente
    for i in range(1, kmax_UM): 
        lista_meds = medidas_UMs[i]
        for meds in lista_meds:
            for k in range(i+1, kmax_med + 1):
                for subset in itertools.combinations(meds, k):
                    if subset not in list_criticos:
                        if checa_ck_med(subset, list_criticos): 
                            count_checks += 1            
                            is_crit = avaliar_candidato(subset, E)
                            if is_crit == True: 
                                list_criticos.append(subset) 
                                medidas_combnts[k-1].append(set(subset))
    return medidas_combnts, count_checks  

    

#Gera combinacoes internas nas criticalidades de UMs
def gera_combinacoes_por_criticalidade(kmax_UM, kmax_med, solution_list, dict_UMs_meds, E):
    medidas_combnts = obter_dicionario_listas(kmax_med)
    list_criticos = list(())
    count_checks = 0
    for k in range(kmax_UM):
        for ckUM in solution_list[k]:
            to_test = list(())
            for i in range(k+1):
                for Med in (dict_UMs_meds[f'{ckUM[i]}']):
                    to_test.append(Med)
            for j in range(k+1, kmax_med +1):
                if j == 3:
                    print()
                for subset in itertools.combinations(to_test, j):
                    if subset not in list_criticos:
                        count_checks += 1
                        if checa_ck_med(subset, list_criticos):
                            is_crit = avaliar_candidato(subset, E)
                            if is_crit == True: 
                                if subset not in list_criticos:
                                    list_criticos.append(subset) 
                                    medidas_combnts[j-1].append(set(subset))
    return medidas_combnts, count_checks


def monta_dicionario_ckmeds_inteligente(kmax_UM, kmax_med, num_cks, solution_list, dict_UMs_meds, E): #saida esperada -> Dicionario por cadinalidade com cks (Identico ao das UMs)
    #Monta dicionario de Medidas envolvidas (por cardinalidade)
    medidas_UMs = obter_dicionario_listas(kmax_UM)
    mod_solution_list = obter_dicionario_listas(kmax_UM)
    for k in range(kmax_UM):
        aux_list = solution_list[k]
        list_to_remove = list(())
        for j in range(len(solution_list[k])):
            UM = aux_list[j]
            if UM not in list_to_remove:   
                for w in range(j+1, len(aux_list)):
                    UM2 = aux_list[w]
                    int_UM = [value for value in UM if value in UM2]
                    if len(int_UM) != 0 and len(int_UM) >= k:
                        UM = sorted(np.unique(UM+UM2))
                        list_to_remove.append(UM2)
                mod_solution_list[k].append(UM)
        for x in range(len(mod_solution_list[k])):
            ckUM = mod_solution_list[k][x]
            list_toAdd = list(())
            for i in range(len(ckUM)):
                list_toAdd.append(dict_UMs_meds[f'{ckUM[i]}'])
            medidas_UMs[k].append(list(set(itertools.chain.from_iterable(list_toAdd))))    
    medidas_UMs[0] = list(set(itertools.chain.from_iterable(medidas_UMs[0])))      
    return medidas_UMs, mod_solution_list



def monta_dicionario_ckmeds(kmax_UM, kmax_med, num_cks, solution_list, dict_UMs_meds, E): #saida esperada -> Dicionario por cadinalidade com cks (Identico ao das UMs)
    #Monta dicionario de Medidas envolvidas (por cardinalidade)
    medidas_UMs = obter_dicionario_listas(kmax_UM)
    for k in range(kmax_UM):
        for ckUM in solution_list[k]:
            for i in range(k+1):
                medidas_UMs[k].append(dict_UMs_meds[f'{ckUM[i]}'])
        medidas_UMs[k] = list(set(itertools.chain.from_iterable(medidas_UMs[k])))
    return medidas_UMs


#filtra criticalidades de cardinalidades superiores que possuem criticaidades de cardinalidades inferiores
def filtra_ck_meds(kmax, dct_ck_med):
    for i in range(len(dct_ck_med)):
        for ckmed in dct_ck_med[i]:
            for k in range (i+1, len(dct_ck_med)):
                aux_list = list(dct_ck_med[k])
                for ckmed2 in aux_list:
                    if set(ckmed).issubset(set(ckmed2)):
                        dct_ck_med[k].remove(ckmed2)
    return dct_ck_med


#checa se um conjunto de medidas possui alguma das criticalidades ja analisadas
def checa_ck_med(med, list_ck_med):
    for ckmed in list_ck_med:
        if set(ckmed).issubset(set(med)):
            return False
    return True


def gera_relatorio_completo(kmax_med, kmax_UM, num_bus, num_meds, dicionario_ckMeds, dicionario_ck_meds_recuperadas,name, num_checks):
    with open('UMs_to_meds'+f'_{name}'+f'_{num_bus}bus' + f'_{num_meds}meds_'+ 'complete' + '.txt', 'w') as f:
        f.write(f'====Measurements Criticality Analysis From Measurement Units Analysis - Complete=====\n')
        f.write(f'kmax_UM = {kmax_UM}\n')
        f.write(f'kmax_med = {kmax_med}\n')
        f.write('\n')
        f.write(f'num checked meds = {num_checks}\n')
        #f.write(f'exec time = {toc - tic} seconds')
        f.write('\n \n')
        # if kmax_UM < kmax_med:
        #    kmax = kmax_UM
        #else:
        #    kmax = kmax_med
        for k in range(kmax_med):
            f.write(f'======================================c{k+1}-Tuples======================================\n')
            f.write(f'num ck-tuples = {len(dicionario_ckMeds[k])}\n\n')
            for elem in dicionario_ckMeds[k]:
                ck = list(elem)
                for i in range(len(ck)):
                    f.write('[%s]'% (ck[i]))
                f.write('\n')
            f.write('\n\n')
            f.write(f'num recovered ck-tuples = {len(dicionario_ck_meds_recuperadas[k])}\n\n')
            for elem in dicionario_ck_meds_recuperadas[k]:
                ck = list(elem)
                for i in range(len(ck)):
                    f.write('[%s]'% (ck[i]))
                f.write('\n') 
        f.close()  
    return


def gera_relatorio_resumido(kmax_med, kmax_UM, num_bus, num_meds, dicionario_ckMeds, dicionario_ck_meds_recuperadas, name, num_checks):
    ddiff = DeepDiff(dicionario_ck_meds_recuperadas, dicionario_ckMeds, ignore_order=True, view = 'tree')      #Compara as criticalidades recuperadas via heurística com as completas
    with open('UMs_to_meds'+f'_{name}'+f'_{num_bus}bus' + f'_{num_meds}meds_' + 'summary' + '.txt', 'w') as f:
        f.write(f'=====Measurements Criticality Analysis From Measurement Units Analysis - Summary=====\n')
        f.write(f'kmax_UM = {kmax_UM}\n')
        f.write(f'kmax_med = {kmax_med}\n')
        f.write('\n')
        f.write(f'num checked meds = {num_checks}\n')
        #f.write(f'exec time = {toc - tic} seconds')
        f.write('\n \n')
        for k in range(kmax_med):
            f.write(f'======================================c{k+1}-Tuples======================================\n')
            f.write(f'num ck-tuples = {len(dicionario_ckMeds[k])}\n\n')
            f.write(f'num recovered ck-tuples = {len(dicionario_ck_meds_recuperadas[k])}\n\n')
        f.write(f'====================================ck-Tuples Missing====================================\n')
        if 'iterable_item_added' in ddiff.keys():
            for tp in ddiff['iterable_item_added']:
                f.write(f'{tp.t2}\n')
        f.close() 
        
        
def printmodCkUMs(num_bus, num_meds, kmax, num_cks, solution_list):

    with open('ck_UMs'+'modified'+f'{num_bus}bus' + f'_{num_meds}meds' + '.txt', 'w') as f:
        f.write(f'=========================Measurement Units Criticality Analysis======================\n')
        f.write(f'kmax = {kmax}')
        f.write('\n \n')
        f.write('\n \n')
        for k in range(kmax):
            f.write(f'======================================c{k+1}-Tuples======================================\n')
            f.write(f'Total c{k+1} tuples = {num_cks[k]}')
            f.write('\n')
            for elem in solution_list[k]:
                ck = list(elem)
                for i in range(len(ck)):
                    f.write('[UM-%s] '% (ck[i]))
                f.write('\n')
            f.write('\n \n')    
    f.close()


if __name__ == "__main__":
    
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    #num_bus = int(input("Digite o num de barras"))
    num_bus = 24
    #Leitura Medicao

    #30 Bus
    #med_file= os.path.join(THIS_FOLDER,'ieee30_observability_PSCC_2014B_43.med')
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
    kmax_med = 4  
    solution_list, num_cks = dfs(E,num_meds,kmax_UM,num_bus,UMs,dict_UMs_meds)
    printCkUMs(num_bus, num_meds, kmax_UM, num_cks, solution_list)

    # Recuperar
    type = 'inteligente'
    match type:
        case 'interna':
            dicionario_ck_meds_recuperadas, num_checks = gera_combinacoes_por_criticalidade(kmax_UM, kmax_med, solution_list, dict_UMs_meds, E)
        case 'mesma':
            medidas_UMs = monta_dicionario_ckmeds(kmax_UM, kmax_med, num_cks, solution_list, dict_UMs_meds, E)
            dicionario_ck_meds_recuperadas, num_checks = gera_combinacoes_mesma_cardinalidade(kmax_UM,kmax_med, medidas_UMs, E) 
        case 'cruzada':
            medidas_UMs = monta_dicionario_ckmeds(kmax_UM, kmax_med, num_cks, solution_list, dict_UMs_meds, E)
            dicionario_ck_meds_recuperadas, num_checks = gera_combinacoes_cardinalidade_cruzada(kmax_UM,kmax_med, medidas_UMs, E)
        case 'inteligente':
            medidas_UMs, mod_solution_list = monta_dicionario_ckmeds_inteligente(kmax_UM, kmax_med, num_cks, solution_list, dict_UMs_meds, E)
            printmodCkUMs(num_bus, num_meds, kmax_UM, num_cks, mod_solution_list)
            dicionario_ck_meds_recuperadas, num_checks = gera_combinacoes_inteligentes(kmax_UM,kmax_med, medidas_UMs, E) 
        


    #Filtrar
    # Percorrer o dionario de cks e remover aquelas que estão contidas em alguma de cardinalidade superior (Cj c Ck onde j<k)
    
    #filtra_ck_meds(kmax_med, dicionario_ck_meds_recuperadas1)
    #filtra_ck_meds(kmax_med, dicionario_ck_meds_recuperadas2)



    # Obtem criticalidades medidas via BF
    number_of_cks_meds, dicionario_ckMeds, sol_list_med_str = meas_criticalities(E,num_meds,kmax_med,num_bus,0,dict_meds)
    

    ##########################################Pós-processo análise Ck-meds######################################## 
    
    
    #Printar as cks recuperadas por cardinalidade
    
  
gera_relatorio_resumido(kmax_med, kmax_UM, num_bus, num_meds, dicionario_ckMeds, dicionario_ck_meds_recuperadas, type, num_checks)
gera_relatorio_completo(kmax_med, kmax_UM, num_bus, num_meds, dicionario_ckMeds, dicionario_ck_meds_recuperadas, type, num_checks)
     
        
print("FIM DO PROGRAMA")



    
   