import numpy as np
import pandas as pd
import subprocess
import os
import itertools


def obtemCaminhoMedicao():

    # Diciona Planos e Redes [Numero Barras : [numbarras,Planos de Medicao Associados,nome caso]]
    dicionarioRedesPlanosMedicao = {

        6 : [[6,'medicao\paper6bus_med_case2.txt','6bus_case2']],

        14 : [[14,'medicao\ieee14_handling_case1.txt','ieee14_handling_case1'],
              [14,'medicao\ieee14_handling_case2.txt','ieee14_handling_case2'],
              [14,'medicao\ieee14_handling_case3.txt','ieee14_handling_case3'],
              [14,'medicao\ieee14_handling_case4.txt','ieee14_handling_case4']],

        30 : [[30, 'medicao\ieee30_observability_PSCC_2014B_43.med','ieee30_observability_PSCC_2014B_43'],
              [30, 'medicao\med30b81m_red_min06.txt','ieee30_81med'],
              [30, 'medicao\med30b97m_red08.txt','ieee30_97med'],
              [30, 'medicao\med30b105m_red_min09.txt','ieee30_105med'],
              [30, 'medicao\med30b_Concentrado_77m_red03.txt', '30_Concentrado77med'],
              [30, 'medicao\med30b_Concentrado100m_red08.txt', '30_Concentrado100med'],
              [30, 'medicao\med30b_Concentrado_112m_red09.txt','30_Concentrado112med'],
              [30, 'medicao\med30_completoInjFlux.txt','30_CompleteMed']           
              ],

        118 : [[118, 'medicao\S1_CS5_352M.med','118_176med'],
               [118, 'medicao\med118b265m_red_min03.txt','118_265med'],
               [118, 'medicao\med118b298m_red_min05.txt','118_298med'],
               [118, 'medicao\med118b442m_red_min09.txt','118_442med'],
               [118, 'medicao\med118b_Concentrado_361m_red03.txt','118_Concentrado361med'],
               [118, 'medicao\med118b_Concentrado410m_red08.txt', '118_Concentrado410med'],
               [118, 'medicao\med118b_Concentrado_448m_red09.txt','118_Concentrado448med'],
               [118, 'medicao\med118_completoInjFlux.txt','118_CompleteMed']           
              ]
    }

    dicionarioRedesPlanosMedicaoBasico={

        6 : [[6,'medicao\paper6bus_med_case2.txt','6bus_case2']],

        14 : [[14,'medicao\ieee14_handling_case1.txt','ieee14_handling_case1'],
              [14,'medicao\ieee14_handling_case2.txt','ieee14_handling_case2'],
              [14,'medicao\ieee14_handling_case3.txt','ieee14_handling_case3'],
              [14,'medicao\ieee14_handling_case4.txt','ieee14_handling_case4']],

        30 : [[30, 'medicao\ieee30_observability_PSCC_2014B_43.med','ieee30_observability_PSCC_2014B_43'],
              [30, 'medicao\med30b81m_red_min06.txt','ieee30_81med'],
              [30, 'medicao\med30b97m_red08.txt','ieee30_97med'],
              [30, 'medicao\med30b105m_red_min09.txt','ieee30_105med'],        
              ],

        118 : [[118, 'medicao\S1_CS5_352M.med','118_176med'],
               [118, 'medicao\med118b265m_red_min03.txt','118_265med'],
               [118, 'medicao\med118b298m_red_min05.txt','118_298med'],
               [118, 'medicao\med118b442m_red_min09.txt','118_442med'],         
              ]
      }


    dicionarioRedesPlanosMedicaoCompleto = {

        6 : [],

        14 : [],

        30 : [[30, 'medicao\med30_completoInjFlux.txt','30_CompleteMed']],

        118 : [[118, 'medicao\med118_completoInjFlux.txt','118_CompleteMed']]
    }


    dicionarioRedesPlanosMedicaoConcentrado = {

        6 : [],

        14 : [],

        30 : [[30, 'medicao\med30b_Concentrado_77m_red03.txt', '30_Concentrado77med'],
              [30, 'medicao\med30b_Concentrado100m_red08.txt', '30_Concentrado100med'],
              [30, 'medicao\med30b_Concentrado_112m_red09.txt','30_Concentrado112med'],         
              ],

        118 : [[118, 'medicao\med118b_Concentrado_361m_red03.txt','118_Concentrado361med'],
               [118, 'medicao\med118b_Concentrado410m_red08.txt', '118_Concentrado410med'],
               [118, 'medicao\med118b_Concentrado_448m_red09.txt','118_Concentrado448med'],     
              ]
       }


        
    return dicionarioRedesPlanosMedicao, dicionarioRedesPlanosMedicaoBasico, dicionarioRedesPlanosMedicaoCompleto, dicionarioRedesPlanosMedicaoConcentrado 
