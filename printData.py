
def printCkUMs(num_bus, num_meds, kmax, num_cks, solution_list):

    with open('ck_UMs'+f'{num_bus}bus' + f'_{num_meds}meds' + '.txt', 'w') as f:
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