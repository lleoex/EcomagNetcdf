from datetime import datetime

import geopandas as gpd
import pandas as pd
import numpy as np

def join_data_to_geom(pixel_data: dict[str: dict[str : dict[int:np.ndarray]]], pixels: np.ndarray):
    geom_file = 'C:\\usr\\data\\emg_rnl\\geo\\cells3857.gpkg'
    geom_data = gpd.read_file(geom_file)
    geom_data['CllId'] = geom_data['CllId'].astype(np.int64)
    gdf = gpd.GeoDataFrame()
    for dts_str in pixel_data:
        qrvr = pixel_data[dts_str]['Qrvr']
        pix_num = len(next(iter(qrvr.values())))
        dates = []
        for dt in qrvr:
            print(f'{datetime.today()}\t{dt}')
            y = dt // 10000
            m = (dt // 100) % 100
            dd = dt % 100
            d = datetime(y, m, dd)
            dates.append(d)
            npd = np.datetime64(d)
            data_arr = np.zeros((pix_num,2))
            date_arr = np.ndarray((pix_num), dtype='datetime64[s]' )
            date_arr.fill(npd)

            for i in range(0,pix_num):
                data_arr[i,0] = pixels[i]
                data_arr[i,1] = qrvr[dt][i]
            dataframe = pd.DataFrame(data_arr, columns=['CllId','qrvr'])
            dateframe = pd.DataFrame(date_arr,columns=['date'])
            resframe = pd.concat([dataframe,dateframe], axis=1)
            resframe['CllId'] = pd.to_numeric(resframe['CllId'], downcast='integer')
            resframe['CllId'] = resframe['CllId'].astype(np.int64)

            finalframe= geom_data.merge(resframe, on='CllId')
            #finalframe.to_file(f'{dt}_res.gpkg',  driver="GPKG")
            gdf = pd.concat([gdf,finalframe])
        print(f'{datetime.today()} \t start writing to file')
        gdf.to_file('res3857.gpkg', driver="GPKG", engine="pyogrio")
        print(f'{datetime.today()} \t end writing to file')

def read_river1():
    file='C:\\usr\\data\\emg_rnl\\river1.csv'
    df = pd.read_csv(file)[['from','to']]

    return df['from'],df['to']







