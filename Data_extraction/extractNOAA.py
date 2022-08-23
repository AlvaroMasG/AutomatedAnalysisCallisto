# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 17:16:42 2022

@author: mas1a
"""

import os
import pandas as pd

contenido = os.listdir('../Data/NOAAtxt')

def main():
    for i in range(0, len(contenido), 1):
        ###Variables
        starthour = []
        startmin = []
        endhour = []
        endmin = []
        duration = []
        seconds = []
        frecstart = []
        frecend = []
        intensity = []
        arrayobs = []
        ###Parametros
        frec = []
        quarterstart = []
        quarterend = []
        partduration = []
        relevance = []
        
        ###Leer ficheros
        txt = read_txt(i)
        fichero = open(txt)
        lineas = fichero.readlines()
        for linea in range(0, len(lineas), 1):
            if linea == 2:
                line = lineas[2]
                day = line[15:17]
                day = int(day)        #dia
                month = line[12:14]
                month = int(month)    #mes
                year = line[7:11]
                year = int(year)       #año
            if linea > 11 and len(lineas[linea]) == 81:
                line = lineas[linea]
                typ = line[43:46]    #tipo RSP
                obs = line[34:37]    #observatorio
                if typ == 'RSP':
                    if obs == 'SVI' or obs == 'CUL' or obs == 'LEA':
                        arrayobs.append(obs)
                        starth = line[11:13]
                        starth = int(starth)
                        starthour.append(starth)
                        startm = line[13:15]
                        startm = int(startm)
                        startmin.append(startm)
                        endh = line[28:30]
                        endh = int(endh)
                        endhour.append(endh)
                        endm = line[30:32]
                        endm = int(endm)
                        endmin.append(endm)
                        fstart = line[48:51]
                        fstart = int(fstart)
                        frecstart.append(fstart)
                        fend = line[52:55]
                        fend = int(fend)
                        frecend.append(fend)
                        dur = (endh - starth)*60 + (endm - startm) + 1
                        duration.append(dur)
                        inten = line[58:63]
                        intensity.append(inten)
        #Parametros
        for v in range(0, len(duration), 1):
            if duration[v] <= 1:
                partduration.append('1P')
            if duration[v] > 1:
                partduration.append('4P')
        
        for k in range(0, len(startmin), 1):
            if startmin[k] < 15:
                quarterstart.append('1Q')
            if startmin[k] >= 15 and startmin[k] < 30:
                quarterstart.append('2Q')
            if startmin[k] >= 30 and startmin[k] < 45:
                quarterstart.append('3Q')
            if startmin[k] >= 45:
                quarterstart.append('4Q')
        
        for l in range(0, len(endmin), 1):
            if endmin[l] < 15:
                quarterend.append('1Q')
            if endmin[l] >= 15 and endmin[l] < 30:
                quarterend.append('2Q')
            if endmin[l] >= 30 and endmin[l] < 45:
                quarterend.append('3Q')
            if endmin[l] >= 45:
                quarterend.append('4Q')
        
        for n in range(0, len(frecend), 1):
            if frecend[n] < 100:
                frec.append('90-15 MHz')
            if frecend[n] >= 100 and frecend[n] < 200:
                frec.append('180-45 MHz')
            if frecend[n] >= 200:
                frec.append('525-110 MHz')
                
        for t in range(0, len(intensity), 1):
            for p in range(0, len(intensity[t]), 1):
                if intensity[t][p] == '1':
                    relevance.append('1')
                if intensity[t][p] == '2':
                    relevance.append('2')
                if intensity[t][p] == '3':
                    relevance.append('3')
                    
        for sec in duration:
            seconds.append(sec*60)
            
        
        #Enviar a Excel
        df = pd.read_excel(r'../Data/BurstData.xlsx')
        for m in range(0, len(starthour), 1):
            df = df.append({'From': 'NOAA',
                                      'Station': arrayobs[m],
                                      'Year': year,
                                      'Month': month,
                                      'Day': day,
                                      'Freq Max (MHz)': frecend[m],
                                      'Freq Min (MHz)': frecstart[m],
                                      'Freq': frec[m],
                                      'Hour Start': starthour[m],
                                      'Min Start': startmin[m],
                                      'Quarter Start': quarterstart[m],
                                      'Duration (min)': duration[m],
                                      'Duration (s)': seconds[m],
                                      'Part Duration': partduration[m],
                                      'Image Start': '-',
                                      'Intensity (dB)': '-',
                                      'Relevance': relevance[m]}, ignore_index=True)
        df.to_excel(r'../Data/BurstData.xlsx', index=False)
    
    
    
    
def read_txt(i):
    
    path = '../Data/NOAAtxt'
    filename = contenido[i]
    
    files = os.path.join(path, filename)
    return files

    
if __name__ == "__main__":
    main()
    print("Proceso finalizado.")
    
