import numpy as np
import pandas as pd

def case_prepare(meds,net,num_bus,num_meds):

    #Monta Adjacencias
    Adj = np.zeros((num_bus,num_bus))
    for i in range(len(net)):
        # print(int(net[i,0]))
        # print(int(net[i,1]))
        Adj[int(net[i,0])-1,int(net[i,1])-1] = 1
        Adj[int(net[i,1])-1,int(net[i,0])-1] = 1

    #Structures Inicialization
    dict_meds={} #med number -> Type of med e.g :"I28"
    UMs = [] #UMs that are activated
    dict_UMs_meds = {} #UM number -> Meds numbers in the UM
    

    #Monta H
    H = np.zeros((num_meds,num_bus),np.float64)
    pmu = 0 #evalue the existence of PMUs
    for m in range(num_meds):

        if meds[m,3] == 1: #Fluxo Ativo
            fr= int(meds[m,0])
            to= int(meds[m,1])
            H[m,fr-1] = 1
            H[m,to-1] =-1
            dict_meds[m] = "P"+ f"{fr}" + "-" + f"{to}" 
            UMs.append(fr)

        if meds[m,3] == 2: #Injecao Ativa
            fr = int(meds[m,0])
            bus_adj = Adj[fr-1,:]
            number_of_conex = 0
            for i in range(num_bus):
                if bus_adj[i] == 1:
                    H[m,i] = -1
                    number_of_conex += 1
            H[m,fr-1] = number_of_conex
            dict_meds[m] = "P"+f"{fr}" 
            UMs.append(fr)

        if meds[m,3] == 3: #Angulo
            fr = int(meds[m,0])
            H[m,fr-1] = 1
            pmu +=1
            dict_meds[m] = "A"+f"{fr}" 
            UMs.append(fr)

        if meds[m,3] == 7: #Corrente
            fr= int(meds[m,0])
            to= int(meds[m,1])
            H[m,fr-1] = 1
            H[m,to-1] =-1
            dict_meds[m] = "I"+ f"{fr}" + "-" + f"{to}"
            UMs.append(fr)
        
        if str(fr) in dict_UMs_meds.keys():
            dict_UMs_meds[str(fr)].append(m) #add a meas for the related UM
        else:
            dict_UMs_meds[str(fr)] = []
            dict_UMs_meds[str(fr)].append(m)

    # Avalia se existem PMUs no plano de Medicao
    if pmu == 0:
        H = np.delete(H, 0, 1)  # delete the first column of H (matrix,number of column/row,column(1)/row(0))
         
    #Monta Relacoes UMs e Meds
    UMs = list(set(UMs)) #remove the duplicates

    return H,dict_meds,dict_UMs_meds,UMs