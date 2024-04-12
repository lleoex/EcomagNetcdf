from binary_reader import BinaryReader
from os import listdir
from os.path import isfile, join
import numpy as np
from nc_functions import CreatePixelNcFile



dir_path = '/home/gonchukov-lv/data/emg_binary/SRV_BIN/'
files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

pixel_vars = ['Qrvr',  'Qlat']
shed_vars =  ['Def',    'EA',            'EB',           'ESUM',      'GwDep', 
              'Pcp',    'QQA',           'QQG',          'QQS', 
              'SnHgt',  'SnWE',          'SoilFrostDep', 'SoilMoist', 'SoilThawDep',
              'SubOutQ','SubSurfWtrDep', 'Tair']

pixel_files = []
shed_files  = []

for file in files:
    vname = file.split('.')[0][:-9:]
    if vname in pixel_vars:
        pixel_files.append(file)
    elif vname in shed_vars:
        shed_files.append(file)

_pixel_data = {}

for file in pixel_files:
    vname = file.split('.')[0][:-9:]
    dts_str = file.split('.')[0][-8::]
    if not dts_str in _pixel_data:
        _pixel_data[dts_str] = {}
    _pixel_data[dts_str][vname] = {}
    with open(dir_path + '/' + file, 'rb') as f:
        reader = BinaryReader(f.read())
        item_count = reader.read_int64()
        Nset = reader.read_int64(item_count)
        net = {}
        for i in range(item_count):
            #Nset[i] = reader.read_int64()
            net[Nset[i]] = i
        
        while(not reader.eof()):
             yyyymmdd = reader.read_int64()
             _pixel_data[dts_str][vname][yyyymmdd] = np.asarray(reader.read_double(item_count))
    #print(file)
CreatePixelNcFile(_pixel_data)
print('hello')





    
              

