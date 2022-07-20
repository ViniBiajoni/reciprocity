#Execute the meas criticalities from the .exe do BF parallel
import numpy as np
import pandas as pd
import subprocess
import os
import itertools
from gera_dados_caso import *
import timeit
import time

#Recieve (E,nmed,kmax,nbar,type_exec)
def meas_criticalities(E,nmed,kmax,nbar,type_exec,dict_meds):
    
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

    if type_exec == 0:
        subprocess.Popen([r"CPU_BF_comp.exe"])
        finished = False
        while finished == False:
            if (os.access("Crits.csv",os.R_OK)):
            # if os.path.exists("Crits.csv"):
            # if kmax == 6 or nbar > 30:
                    # time.sleep(5)
                finished = True
            # else:
            #     print("The file does not exist yet")
        # time.sleep(1)
        file_crits= 'Crits.csv'
        colNames=['Criticalidades']
        crits =  pd.read_csv(file_crits,names=colNames)
        j=0
        card = []
        integer_list = []
        ############################Monta Dicionario por Cardinalidade c/ as Criticalidades de Medidas########################################
        crits = pd.read_csv(file_crits,names=colNames) # leitura nova para considerar o fim do print do csv
        for c in crits['Criticalidades']:
            temp=c.split()
            integer_map = map(int, temp)
            integer_list.append(list(integer_map))
            card.append(len(integer_list[j]))
            j=j+1
            card_max= max(card)

        keys = list(range(kmax))
        sol_list_med_number = {key: [] for key in keys}
        sol_list_med_str = {key: [] for key in keys} #create the list with the criticalities strings
        for ck in integer_list:
            tupla=[]
            temp =[]
            for i in ck:
                tupla.append(i)
                temp.append(dict_meds[int(i)])
            sol_list_med_number[len(ck)-1].append(set(tupla))
            sol_list_med_str[len(ck)-1].append(temp)

        #############################Number of Criticalities per Cardinality################
        number_of_cks_meds = [card.count(i+1) for i in range(kmax)]

    if type_exec == 1:
        if os.path.exists("CritsBase.txt"):
            os.remove("CritsBase.txt") 
        else:
            print("The file does not exist yet")
        subprocess.Popen([r"CPU_BF_simp.exe"])
        finished = False
        while finished == False:
            if os.path.exists("CritsBase.txt"):
                if kmax == 6 or nbar > 30:
                    time.sleep(5)
                break 
        time.sleep(1)
        sol_list_med_number = []
        sol_list_med_str = []
        number_of_cks_meds = np.loadtxt("CritsBase.txt")
    
    return number_of_cks_meds, sol_list_med_number,sol_list_med_str

def main():
    # Este Programa Prepara a Leitura de Casos dos Algoritmos
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    num_bus = int(input("Digite o num de barras"))


    #Leitura Medicao

    #6 Bus
    # med_file= os.path.join(THIS_FOLDER,'medicao\paper6bus_med_case2.txt')

    #14 Bus
    # med_file= os.path.join(THIS_FOLDER,'medicao\ieee14_handling_case1.txt')
    # med_file= os.path.join(THIS_FOLDER,'medicao\ieee14_handling_case2.txt')
    # med_file= os.path.join(THIS_FOLDER,'medicao\ieee14_handling_case3.txt')
    # med_file= os.path.join(THIS_FOLDER,'medicao\ieee14_handling_case4.txt')
    # caso = 'ieee14_handling_case1'

    #24 Barras
    med_file= os.path.join(THIS_FOLDER,'24BusUM10eUM15.med')
    caso = '24BusUM10eUM15'


    #30 Bus
    #med_file= os.path.join(THIS_FOLDER,'ieee30_observability_PSCC_2014B_43.med')
    # med_file= os.path.join(THIS_FOLDER,'medicao\med30b81m_red_min06.txt')
    # med_file= os.path.join(THIS_FOLDER,'medicao\med30b105m_red_min09.txt')
    #caso = 'ieee30_observability_PSCC_2014B_43'
    # caso = 'ieee30_81med'
    # caso = 'ieee30_105med'

    #IEEE 118
    # med_file= os.path.join(THIS_FOLDER,'medicao\S1_CS5_352M.med')
    # med_file= os.path.join(THIS_FOLDER,'medicao\med118b265m_red_min0.3.txt')
    # med_file= os.path.join(THIS_FOLDER,'medicao\med118b298m_red_min0.5.txt')
    # med_file= os.path.join(THIS_FOLDER,'medicao\med118b442m_red_min0.9.txt')
    # caso = '118_352med'
    # caso = '118_265med'
    #caso = '118_298med'
    # caso = '118_442med'
    
    meds= np.loadtxt(med_file)
    num_meds = len(meds[:,0])
    #Leitura Sistema
    #net_file= os.path.join(THIS_FOLDER,'sistemas\paper6Bus_case2.txt')
    # net_file= os.path.join(THIS_FOLDER,'sistemas\ieee14.txt')
    net_file= os.path.join(THIS_FOLDER,'sistemas\ieee24.txt')
    # net_file= os.path.join(THIS_FOLDER,'sistemas\ieee30.txt')
    # net_file= os.path.join(THIS_FOLDER,'sistemas\ieee118.txt')24
    net = np.loadtxt(net_file)

    #Monta H e esturura de relacoes entre medidas e UMs
    H,dict_meds,dict_UMs_meds,UMs = case_prepare(meds,net,num_bus,num_meds)

    #Monta G e E
    G =  np.transpose(H)@H
    E = np.identity(num_meds) - H@(np.linalg.inv(G))@np.transpose(H)
    kmax=4
    type_exec = 0 # 0 is a complete sim and 1 is a simplified
    tic= timeit.default_timer()
    number_of_cks_meds, sol_list_med_number, sol_list_med_str = meas_criticalities(E,num_meds,kmax,num_bus,type_exec,dict_meds)
    toc = timeit.default_timer()
    # print(number_of_cks_meds)
    ############################################RESULTS##########################################
    with open('ck_meds'+f'{num_bus}bus' + f'_{num_meds}meds_' + caso + '.txt', 'w') as f:
        f.write(f'=========================Measurements Criticality Analysis===========================\n')
        f.write(f'kmax = {kmax}')
        f.write('\n')
        f.write(f'exec time = {toc - tic} seconds')
        f.write('\n \n')
        for k in range(kmax):
            f.write(f'======================================c{k+1}-Tuples======================================\n')
            f.write(f'num ck-tuples = {len(sol_list_med_str[k])}\n\n')
            for elem in sol_list_med_str[k]:
                ck = list(elem)
                for i in range(len(ck)):
                    f.write('[%s]'% (ck[i]))
                    # f.write('%s '% (sol_list_med_number[k][i]))
                f.write('\n')
            f.write('\n \n')    
    f.close()
    print("FINISHED")
if __name__ == "__main__":
    main()