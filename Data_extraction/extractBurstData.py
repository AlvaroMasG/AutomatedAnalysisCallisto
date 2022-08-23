# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 17:16:42 2022

@author: mas1a
"""

import numpy as np
import pandas as pd
import pyfits
import matplotlib.pyplot as plt 
from matplotlib import cm
import sunpy
import sunpy.data.sample
from radiospectra.sources.callisto import CallistoSpectrogram
import os

contenido = os.listdir('../Data/Image')

def main():
    for i in range(0, len(contenido), 1):
        ###Variables
        position_start = []
        position_start2 = [] #Variable start rafaga
        position_end = []
        position_end2 = [] #Variable end rafaga
        quarter_start = [] #Variable quarter start
        quarter_end = [] #Variable quarter end
        relevance = [] #Intensidad por partes
        part_duration = [] #Variable part duration
        goover = 0
        count = 0
        dB_end = 0
        d = 0
        e = 1
        array_time = [] #Valores interesantes
        discard = [] #Valores de ruido
        array_start = [] #Valores inicio de burst final
        array_start2 = [] #Valores inicio de burst apoyo
        array_end = [] #Valores final de burst final
        array_end2 = [] #Valores final de burst apoyo
        array_duration = [] #Valores duracion del burst apoyo
        array_duration2 = [] #Valores duracion del burst final
        array_dB = [] #Valores dB del burst apoyo
        array_dB2 = [] #Valores dB del burst final
        frec = [] #Rango de frecuencias
        minutes = [] #Duracion en minutos
        
        ###Leer ficheros
        fds = read_py(i)
        image = read_image(i)
        
        ###Extraer datos de los ficheros
        #py
        data = fds[0].data
        data = data - data.mean(axis=1, keepdims=True) + 4 # subtract mean and add offset (1...50)
        data = data.clip(-5,120) # limit peak values
        data = data * 2500.0/255.0/25.4 # digit->dB
        datameanhor = np.mean(data, axis=1)
        #image
        station = str(image.instruments)
        station = station[2:-2]
        date = str(image.start)
        date = date[:10]
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:10])
        start = fds[0].header['TIME-OBS']
        start_hour = int(start[:2])
        start_minutes = int(start[3:5])
        start_seconds = int(start[6:8])
        start_title = str(start[:8])
        end = fds[0].header['TIME-END']
        end_hour = int(end[:2])
        end_minutes = int(end[3:5])
        end_seconds = int(end[6:8])
        end_title = str(end[:8])
        freq_min = int(min(image.freq_axis))
        freq_max = int(max(image.freq_axis))
        lat = fds[0].header['OBS_LAT']
        lac = fds[0].header['OBS_LAC']
        lon = fds[0].header['OBS_LON']
        loc = fds[0].header['OBS_LOC']
        alt = fds[0].header['OBS_ALT']
        
        ###Dibuja el .fit
        freqs = fds[1].data['frequency'][0]
        time = fds[1].data['time'][0]
        extent = (time[0], time[-1], freqs[-1], freqs[0])
        plt.imshow(data, aspect = 'auto', extent = extent,cmap=cm.hot)
        plt.xlabel('Time [s]')
        plt.ylabel('Frequency [MHz]')
        plt.title('Type III burst with background subtracted')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('dB above background')
        plt.show()
        
        ###Filtros
        #Examinar horizontalmente y eliminar filtros
        for a in datameanhor:
            if a > datameanhor[0] + (1/2) or a < datameanhor[0] - (1/2):
                discard.append(goover)
            goover += 1
            
        #Eliminar elementos y meter verticalmente sin ruido
        data2 = np.delete(data, tuple(discard), axis = 0)
        datameanver = np.mean(data2, axis = 0)

        #Analizar verticalmente. Obtener datos interesantes
        for b in datameanver:
            if b > datameanhor[0] + (1/2):
                array_time.append(count)
            count += 1
            
            
        ###Dibujar lightcurve
        plt.plot(image.time_axis,datameanver,linewidth=1.0)
        plt.ylabel('Y-factor [dB]')
        plt.xlabel('Time [seconds]')
        title = ('Lightcurve of {}. Date: {}. Start: {}. End: {}'.format(station, date, start_title, end_title))
        print('Title: ',title)
        plt.title(title)
        plt.grid(True)
        plt.plot()
        plt.show()
        
        ###Procesar datos de Excel
        #Start, End and Duration
        for h in array_time:
            if  d == 0 or array_time[d] + 15 < array_time[e]:
                if e >= len(array_time):
                    array_start.append(array_time[d])
                elif e < len(array_time):
                    array_start.append(array_time[e])
            if d == len(array_time)-1 or array_time[d] + 15 < array_time[e]:
                array_end.append(array_time[d])
            d += 1
            e += 1
            if e >= len(array_time):
                e -= 1
        
        len_as = len(array_start)
        #Start, End and Duration de nuevo y dB
        for j in range(0, len_as, 1):
            duration = array_end[j] - array_start[j]
            if duration > 5:
                array_duration.append(duration)
                array_start2.append(array_start[j])
                array_end2.append(array_end[j])
                for z in range(array_start[j], array_end[j], 1):
                    if datameanver[z] > dB_end:
                        dB_end = datameanver[z]
                array_dB.append(dB_end)
                dB_end = 0
                
        #Position
        for k in array_start2:
            if k < 720:
                position_start.append("FL")
            if k >= 720 and k < 1440:
                position_start.append("L")
            if k >= 1440 and k < 2160:
                position_start.append("C")
            if k >= 2160 and k < 2880:
                position_start.append("R")
            if k >= 2880:
                position_start.append("FR")
                
        for k in array_end2:
            if k < 720:
                position_end.append("FL")
            if k >= 720 and k < 1440:
                position_end.append("L")
            if k >= 1440 and k < 2160:
                position_end.append("C")
            if k >= 2160 and k < 2880:
                position_end.append("R")
            if k >= 2880:
                position_end.append("FR")
                
        for n in range(0, len(array_start2), 1):
            array_start2[n] = int(array_start2[n]*(0.25))
            array_end2[n] = int(array_end2[n]*(0.25))
            array_duration[n] = int(array_duration[n]*0.25)
            
        #Filtro para terminar teniendo burst con el dB pico > 2.4
        array_start = []
        array_end = []
        
        for l in range(0, len(array_dB), 1):
            if array_dB[l] > 2.4:
                array_start.append(array_start2[l])
                array_end.append(array_end2[l])
                array_duration2.append(array_duration[l])
                array_dB2.append(array_dB[l])
                position_start2.append(position_start[l])
                position_end2.append(position_end[l])
        
        for minu in array_duration2:
            minutes.append(minu/60)
                
        #Importancia del burst detectado, segun la intensidad
        for p in range(0, len(array_dB2), 1):
            if array_dB2[p] < 3:
                relevance.append('1')
            if array_dB2[p] >= 3 and array_dB2[p] < 5:
                relevance.append('2')
            if array_dB2[p] >= 5 and array_dB2[p] < 10:
                relevance.append('3')
            if array_dB2[p] >= 10:
                relevance.append('3')
                
        #Importancia de la duracion
        for v in range(0, len(array_duration2), 1):
            if array_duration2[v] < 5:
                part_duration.append('1P')
            if array_duration2[v] >= 5 and array_duration2[v] < 15:
                part_duration.append('2P')
            if array_duration2[v] >= 15 and array_duration2[v] < 60:
                part_duration.append('3P')
            if array_duration2[v] >= 60:
                part_duration.append('4P')
                
        #Minuto que ocurre el burst detectado
        for t in range(0, len(array_start), 1):
            array_start[t] = start_minutes + array_start[t]/60
            array_end[t] = start_minutes + array_end[t]/60
            if array_start[t] < 15:
                quarter_start.append('1Q')
            if array_start[t] >= 15 and array_start[t] < 30:
                quarter_start.append('2Q')
            if array_start[t] >= 30 and array_start[t] < 45:
                quarter_start.append('3Q')
            if array_start[t] >= 45:
                quarter_start.append('4Q')
            if array_end[t] < 15:
                quarter_end.append('1Q')
            if array_end[t] >= 15 and array_end[t] < 30:
                quarter_end.append('2Q')
            if array_end[t] >= 30 and array_end[t] < 45:
                quarter_end.append('3Q')
            if array_end[t] >= 45:
                quarter_end.append('4Q')
        
        #Rango de frecuencia
        if freq_max < 100:
            frec = '90-15 MHz'
        if freq_max >= 100 and freq_max < 200:
            frec = '180-45 MHz'
        if freq_max >= 200:
            frec = '525-110 MHz'
            
        
        #Enviar a Excel
        df = pd.read_excel('../Data/BurstData.xlsx')
        for m in range(0, len(array_start), 1):
            df = df.append({'From': 'e-Callisto',
                                      'Station': station, 
                                      'Year': year,
                                      'Month': month,
                                      'Day': day,
                                      'Freq Max (MHz)': freq_max,
                                      'Freq Min (MHz)': freq_min,
                                      'Freq': frec,
                                      'Hour Start': start_hour,
                                      'Min Start': array_start[m],
                                      'Quarter Start': quarter_start[m],
                                      'Duration (min)': minutes[m],
                                      'Duration (s)': array_duration2[m],
                                      'Part Duration': part_duration[m],
                                      'Image Start': position_start2[m],
                                      'Intensity (dB)': array_dB2[m],
                                      'Relevance': relevance[m]}, ignore_index=True)
        df.to_excel('../Data/BurstData.xlsx', index=False)
        
    
def read_py(i):
    
    path = '../Data/Image'
    filename = contenido[i]
    
    files = os.path.join(path, filename)
    fds = pyfits.open(files)
    return fds

def read_image(i):
    
    path = '../Data/Image'
    filename = contenido[i]
    
    files = os.path.join(path, filename)
    image = CallistoSpectrogram.read(files)
    return image
    
if __name__ == "__main__":
    main()
    print("Proceso finalizado.")
    
