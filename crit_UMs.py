#Execute the meas criticalities from the .exe do BF parallel
import numpy as np
import pandas as pd
import subprocess
import os
import itertools
from gera_dados_caso import *
import scipy
import scipy.linalg
import timeit
from collections import deque
#Recieve (E,nmed,kmax,nbar,type_exec)

def dfs(E,nmed,kmax,nbar,UMs,dicUMs_meas):
    x_0 = len(UMs)*[0]
    keys = list(range(kmax))
    sol_list = {key: [] for key in keys}
    active_list = []
    active_list.append(x_0)

    while active_list != []:
        x = active_list.pop() # catches the top of teh stack
        active_list, sol_list = branch(x,E,kmax,UMs,active_list,dicUMs_meas,sol_list)

    num_cks = [len(sol_list[i]) for i in range(kmax)]
    return sol_list,num_cks

def bfs(E,nmed,kmax,nbar,UMs,dicUMs_meas):
    x_0 = len(UMs)*[0]
    keys = list(range(kmax))
    sol_list = {key: [] for key in keys}
    active_list = deque()
    active_list.append(x_0)

    while active_list != []:
        x = active_list.popleft() # catches the top of teh stack
        active_list, sol_list = branch(x,E,kmax,UMs,active_list,dicUMs_meas,sol_list)

    num_cks = [len(sol_list[i]) for i in range(kmax)]
    return sol_list,num_cks


def branch(x,E,kmax,UMs,active_list,dicUMs_meas,sol_list):
    k_atual = sum(x)
    # print(f'============c{k_atual+1}===========')
    if k_atual < kmax:
        pos = len(UMs) -1
        while (x[pos] != 1):
            x[pos] = 1
            x_teste = x.copy()
            is_crit = bound(x_teste,E,kmax,active_list,dicUMs_meas,UMs)

            if is_crit == 0: #not criticaL
                active_list.append(x_teste)
            if is_crit ==1: #critical ck-tuplas
                ck_UMs = [x_teste*UMs for x_teste,UMs in zip(x_teste,UMs)]
                ck_UMs = [i for i in ck_UMs if i != 0]
                # print(ck_UMs)
                # print("\n")
                sol_list[k_atual].append(ck_UMs)
            # if is_crit > 1: #cj is in ck 
            if pos == 0:
                break
            x[pos] = 0
            pos = pos - 1
            
    return active_list,sol_list 

def bound(x_teste,E,kmax,active_list,dicUMs_meas,UMs):
    
    k_atual = sum(x_teste)
    is_crit = 0
    if k_atual <= kmax:
        is_crit = eval_crit(x_teste,dicUMs_meas,UMs,E)
        if is_crit > 0 and k_atual > 1:
            pos = len(UMs) - 1
            while (is_crit < 2) and (pos>=0):
                if x_teste[pos] == 1:
                    x_teste[pos] = 0
                    is_crit = is_crit + eval_crit(x_teste,dicUMs_meas,UMs,E)
                    x_teste[pos] = 1
                pos = pos - 1
    return is_crit

def eval_crit(x_teste,dicUMs_meas,UMs,E):
    UMs_desactivated = [x_teste*UMs for x_teste,UMs in zip(x_teste,UMs)]
    UMs_desactivated = [i for i in UMs_desactivated if i != 0]
    #Obtain the meas envolved in the ck-tuple
    meas_envolved = []
    for i in UMs_desactivated:
        meas_envolved.append(dicUMs_meas[str(i)])
    #Desencadeia Listas
    meas_envolved = list(itertools.chain.from_iterable(meas_envolved))
    n_meas = len(meas_envolved)
    E_aux = np.zeros((n_meas,n_meas))
    for i in range(n_meas):
        E_aux[i,i] = E[meas_envolved[i],meas_envolved[i]]
        for j in range(i+1,n_meas):
            E_aux[i,j] = E[meas_envolved[i],meas_envolved[j]]
            E_aux[j,i] = E_aux[i,j]

    P, L, U = scipy.linalg.lu(E_aux)

    is_crit = 0

    if min(abs(np.diag(U))) < 1e-10:

        is_crit = 1
    
    return is_crit

def main():
    # Este Programa Prepara a Leitura de Casos dos Algoritmos
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    num_bus = int(input("Digite o num de barras"))
    #Leitura Medicao
    med_file= os.path.join(THIS_FOLDER,'medicao\ieee30_observability_PSCC_2014B_43.med')
    # med_file= os.path.join(THIS_FOLDER,'medicao\paper6bus_med_case2.txt')
    meds= np.loadtxt(med_file)
    num_meds = len(meds[:,0])
    #Leitura Sistema
    net_file= os.path.join(THIS_FOLDER,'sistemas\ieee30.txt')
    # net_file= os.path.join(THIS_FOLDER,'sistemas\paper6Bus_case2.txt')
    net = np.loadtxt(net_file)

    #Monta H e esturura de relacoes entre medidas e UMs
    H,dict_meds,dict_UMs_meds,UMs = case_prepare(meds,net,num_bus,num_meds)

    #Monta G e E
    G =  np.transpose(H)@H
    E = np.identity(num_meds) - H@(np.linalg.inv(G))@np.transpose(H)
    kmax=3
    tic = timeit.default_timer()
    solution_list, num_cks = dfs(E,num_meds,kmax,num_bus,UMs,dict_UMs_meds)
    toc = timeit.default_timer()
    ############################################RESULTS##########################################
    with open('ck_UMs'+f'{num_bus}bus' + f'_{num_meds}meds' + '.txt', 'w') as f:
        f.write(f'=========================Measurement Units Criticality Analysis======================\n')
        f.write(f'kmax = {kmax}')
        f.write('\n \n')
        f.write(f'exec time = {toc - tic} seconds')
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
    print("Finished")


if __name__ == "__main__":
    main()