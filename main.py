from binary_reader import BinaryReader
from os import listdir
from os.path import isfile, join

dir_path = '/home/gonchukov-lv/data/emg_binary/20200825/SRV_BIN'
files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

for file in files:
    vname = file.split('.')[0][:-9:]
    print(vname)