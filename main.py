from binary_reader import BinaryReader
from os import listdir
from os.path import isfile, join
import numpy as np
from nc_functions import CreatePixelNcFile, CreateShedNcFile
from config import pixel_vars, shed_vars
from geopack import read_river1
from datetime import datetime



def get_vname_dts_str(file: str):
    vname = file.split('.')[0][:-9:]
    dts_str = file.split('.')[0][-8::]
    return vname, dts_str

def read_file(dir_path,file):
    result = {}
    with open(dir_path + '/' + file, 'rb') as f:
        reader = BinaryReader(f.read())
        item_count = reader.read_int64()
        Nset = reader.read_int64(item_count)

        while (not reader.eof()):
            yyyymmdd = reader.read_int64()
            result[yyyymmdd] = np.asarray(reader.read_double(item_count))
            #print(f'{file};{yyyymmdd};{result[yyyymmdd].min()};{result[yyyymmdd].max()};{result[yyyymmdd].mean()}'.replace('.',','))
    return result,Nset

def read_file4(dir_path,file):
    result = {}
    with open(dir_path + '/' + file, 'rb') as f:
        reader = BinaryReader(f.read())
        item_count = reader.read_int32()
        Nset = reader.read_int32(item_count)

        while (not reader.eof()):
            yyyymmdd = reader.read_int32()
            result[yyyymmdd] = np.asarray(reader.read_float(item_count))
            #print(f'{file};{yyyymmdd};{result[yyyymmdd].min()};{result[yyyymmdd].max()};{result[yyyymmdd].mean()}'.replace('.',','))
    return result,Nset

def read_files(filelist, kind=8):
    result = {}
    for file in filelist:
        vname, dts_str = get_vname_dts_str(file)
        if not dts_str in result:
            result[dts_str] = {}
        if kind == 8:
            data, Nset = read_file(dir_path, file)
        elif kind == 4:
            data, Nset = read_file4(dir_path, file)
        result[dts_str][vname] = data
    return result, Nset

#dir_path = '/home/gonchukov-lv/data/emg_binary/SRV_BIN/'
dir_path = 'C:\\usr\\data\\emg_rnl\\burea2003-2004_float32'
files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]



pixel_files = []
shed_files  = []

for file in files:
    vname = file.split('.')[0][:-9:]
    if vname in pixel_vars:
        pixel_files.append(file)
    elif vname in shed_vars:
        shed_files.append(file)

_from, _to = read_river1()
_from_to = np.stack([_from, _to], axis=-1)

_pixel_data, pix_nset = read_files(pixel_files, kind=4)

rev_nset = {}
for i in range(len(pix_nset)):
    rev_nset[pix_nset[i]] = i

for dts_str in _pixel_data:
    with open(f'{dts_str}_res.csv','wt') as f:
        f.write(f'dt,cllid,dqdx\n')
        qrvr = _pixel_data[dts_str]['Qrvr']
        pix_num = len(next(iter(qrvr.values())))
        for dt in qrvr:
            print(dt)
            dqdx = np.zeros_like(qrvr[dt])
            residuals = np.copy(qrvr[dt])
            for i in range(_from_to.shape[0]):
                _from_cllid,_to_cllid = _from_to[i,:]
                _from_idx = rev_nset[_from_cllid]
                _to_idx = rev_nset[_to_cllid]

                _from_q =qrvr[dt][_from_idx]
                _to_q = qrvr[dt][_to_idx]

                residuals[_to_idx] = residuals[_to_idx] - _from_q
                dqdx[_to_idx] = residuals[_to_idx]

            for i in range(pix_num):
                cllid = pix_nset[i]
                f.write(f'{dt},{cllid},{dqdx[i]}\n')





        f.close();

#join_data_to_geom(_pixel_data, pix_nset)

#_shed_data, shed_nset = read_files(shed_files)

#CreateShedNcFile(_shed_data, shed_nset)

#CreatePixelNcFile(_pixel_data, pix_nset)





    
              

