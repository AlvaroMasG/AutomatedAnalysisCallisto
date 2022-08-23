# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 17:21:38 2022

@author: mas1a
"""

import os
import pyfits

contenido = os.listdir('../Data/Image')  
path = '../Data/Image'

station = ''
files2 = ''
flag = 0

##to delete the files of an antenna, by the code
#for py_file in contenido:
#    if py_file[-9:-7] == "04":
#        files = os.path.join(path, py_file)
#        os.remove(files)

for py_file in contenido:
    if py_file[-16:-13] == "235":
        files = os.path.join(path, py_file)
        os.remove(files)
    if py_file[-16:-13] == "234":
        files = os.path.join(path, py_file)
        os.remove(files)
        
for py_file in contenido:
    files = os.path.join(path, py_file)
    fds = pyfits.open(files)
    file_size = os.path.getsize(files)
    
    if flag == 1:
        os.remove(files2)
    
    flag = 0
    files2 = files
    station = str(fds[0].header['INSTRUME'])
    
    if station == 'ALASKA-HAARP' or station == 'GERMANY-DLR' or station == 'KRIM':
        if file_size <= 50000:
            flag = 1
    elif station == 'ALASKA-COHOE' or station == 'ALMATY' or station == 'AUSTRIA-Krumbach' or station == 'AUSTRIA-OE3FLB' or station == 'Australia-ASSA' or station == 'Australia-LMRO' or station == 'INDIA-GAURI' or station == 'GLASGOW' or station == 'INDIA-OOTY' or station == 'INDIA-UDAIPUR' or station == 'JAPAN-IBARAKI' or station == 'KASI' or station == 'SOUTHAFRICA-SANSA' or station == 'USA-ARIZONA-ERAU':
        if file_size <= 120000:
            flag = 1
    elif station == 'ALASKA-ANCHORAGE' or station == 'AUSTRIA-MICHELBACH' or station == 'DENMARK' or station == 'MEXART' or station == 'MRO' or station == 'ROSWELL-NM' or station == 'SPAIN-PERALEJOS' or station == 'SWISS-IRSOL' or station == 'TRIEST':
        if file_size <= 165000:
            flag = 1
    elif station == 'ALGERIA-CRAAG' or station == 'AUSTRIA-UNIGRAZ' or station == 'GREENLAND' or station == 'HURBANOVO' or station == 'INDONESIA' or station == 'SPAIN-ALCALA' or station == 'SPAIN-SIGUENZA' or station == 'SWISS-HB9SCT' or station == 'URUGUAY':
        if file_size <= 190000:
            flag = 1
    elif station == 'SWISS-Landschlacht' or station == 'SWISS-MUHEN':
        if file_size <= 240000:
            flag = 1
    
    station = ''
    
        