import numpy as np
import os
from gera_dados_caso import *
from crit_UMs import dfs
import numpy as np

if __name__ == "__main__":
    
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    num_bus = int(input("Digite o num de barras"))

    #Leitura Medicao

    #30 Bus
    med_file= os.path.join(THIS_FOLDER,'medicao\ieee30_observability_PSCC_2014B_43.med')
    caso = 'ieee30_observability_PSCC_2014B_43'

    meds= np.loadtxt(med_file)
    num_meds = len(meds[:,0])

    #Leitura Sistema
    # net_file= os.path.join(THIS_FOLDER,'sistemas\ieee14.txt')
    net_file= os.path.join(THIS_FOLDER,'sistemas\ieee30.txt')
    net = np.loadtxt(net_file)

    #Monta H e esturura de relacoes entre medidas e UMs
    H,dict_meds,dict_UMs_meds,UMs = case_prepare(meds,net,num_bus,num_meds)

    #Monta G e E
    G =  np.transpose(H)@H
    E = np.identity(num_meds) - H@(np.linalg.inv(G))@np.transpose(H)

    #Call crit UMs analysis
    kmax = 4 
    solution_list, num_cks = dfs(E,num_meds,kmax,num_bus,UMs,dict_UMs_meds)
    
   