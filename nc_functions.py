import datetime
import os.path

import netCDF4 as nc
import numpy as np
from datetime import datetime
from cftime import num2date, date2num

import config


def CreatePixelNcFile(pixel_data: dict[str: dict[str : dict[int:np.ndarray]]], pixels: np.ndarray, res_dir = ""):
    for dts_str in pixel_data:
        if len(pixel_data[dts_str]) == 2:
            qlat = pixel_data[dts_str]['Qlat']
            qrvr = pixel_data[dts_str]['Qrvr']
        else:
            qrvr = pixel_data[dts_str]['Qrvr']
            qlat = qrvr
            
            if len(qlat) == len(qrvr):
                dates = []
                for dt in qlat:
                    y = dt//10000
                    m = (dt//100)%100
                    dd = dt%100
                    d = datetime(y, m,dd)
                    dates.append(d)
                fname = f'River_{dts_str}.nc'
                fpath = os.path.join(res_dir, fname)

                pix_num = len(next(iter(qlat.values())))
                ds = nc.Dataset(fpath,'w', format='NETCDF4')
                ds.createDimension('time', None)
                ds.createDimension('pixels', pix_num)

                time_var = ds.createVariable('time_val','f4',('time',))
                time_var.units = f'days since {dates[0]}'
                time_var.calendar = 'standard'
                dates_val = date2num(dates,time_var.units , time_var.calendar )
                time_var[:] = dates_val

                pix_var = ds.createVariable('pixel_ids','i4',('pixels',))
                pix_var.units = ''
                pix_var.long_name = 'id of river network segment'
                pix_var[:] = pixels

                qrvr_var = ds.createVariable('Qrvr', 'f4', ('time','pixels',),compression='zlib',
                                             significant_digits=4)
                qrvr_var.units = 'm3 s-1'
                qrvr_var.long_name='water_volume_transport_in_river_channel'
                qrvr_var.meta_var_id = '48'

                qrvr_arr_lst = list(qrvr.values())
                qrvr_arr = np.vstack(qrvr_arr_lst)
                qrvr_var[:] = qrvr_arr

                qlat_var = ds.createVariable('Qlat', 'f4', ('time', 'pixels',), compression='zlib',
                                             significant_digits=4)
                qlat_var.units = 'm3 s-1'
                qlat_var.long_name = 'incoming_water_volume_transport_along_river_channel'
                qlat_var.meta_var_id = '48'

                qlat_arr_lst = list(qlat.values())
                qlat_arr = np.vstack(qlat_arr_lst)
                qlat_var[:] = qlat_arr

                ds.close()


def CreateShedNcFile(shed_data: dict[str: dict[str: dict[int:np.ndarray]]], pixels: np.ndarray, res_dir = ""):
     vars = ['Def', 'EA', 'EB', 'ESUM', 'GwDep',
                  'Pcp', 'QQA', 'QQG', 'QQS',
                  'SnHgt', 'SnWE', 'SoilFrstDep', 'SoilMoist', 'SoilThawDep',
                  'SubOutQ',
             'SubSurfWtrDep', 'Tair']


     # vars = [ 'SnWE']
     for dts_str in shed_data:
        dates = []
        firstVar = list(shed_data[dts_str].keys())[0]
        for dt in shed_data[dts_str][firstVar]:
            y = dt // 10000
            m = (dt // 100) % 100
            dd = dt % 100
            d = datetime(y, m, dd)
            dates.append(d)

        fname =f'Sheds_{dts_str}.nc'
        fpath = os.path.join(res_dir,fname)


        shed_num = len(pixels)
        ds = nc.Dataset(fpath, 'w', format='NETCDF4')
        ds.createDimension('time', None)
        ds.createDimension('watersheds', shed_num)

        time_var = ds.createVariable('time', 'f4', ('time',))
        time_var.units = f'days since {dates[0]}'
        time_var.calendar = 'standard'
        dates_val = date2num(dates, time_var.units, time_var.calendar)
        time_var[:] = dates_val

        sheds_var = ds.createVariable('watersheds', 'i4', ('watersheds',))
        sheds_var.units = ''
        sheds_var.long_name = 'id of watershed'
        sheds_var[:] = pixels

        ds.institution = 'The Water Problems Institute of the Russian Academy of Sciences'
        ds.source = 'ECOMAG NGMS 2024 v1'

        for var_name in vars:
            if(var_name in shed_data[dts_str]):
                nc_var = ds.createVariable(var_name, 'f4', ('time', 'watersheds',), compression='zlib',
                                             least_significant_digit=4)
                #nc_var.units = 'm3 s-1'
                if var_name in config.vars_long_names:
                    nc_var.long_name = config.vars_long_names[var_name]
                else:
                    nc_var.long_name = var_name

                if var_name in config.vars_units:
                    nc_var.units = config.vars_units[var_name]
                else:
                    nc_var.units = var_name






                arr_lst = list(shed_data[dts_str][var_name].values())
                arr = np.vstack(arr_lst)
                nc_var[:] = arr

        ds.close()


def CreateNcFile(data: dict[str: dict[str: dict[int:np.ndarray]]], Nset: np.ndarray, isWatersheds:bool, res_dir=""):

    Nset_name ='pixels'
    if isWatersheds:
        Nset_name = 'watersheds'


    for dts_str in data:
        dates = []
        firstVar = list(data[dts_str].keys())[0]
        for dt in data[dts_str][firstVar]:
            y = dt // 10000
            m = (dt // 100) % 100
            dd = dt % 100
            d = datetime(y, m, dd)
            dates.append(d)


        if isWatersheds:
            fname = f'Sheds_{dts_str}.nc'
        else:
            fname = f'River_{dts_str}.nc'


        fpath = os.path.join(res_dir, fname)

        nset_num = len(Nset)
        ds = nc.Dataset(fpath, 'w', format='NETCDF4')
        ds.createDimension('time', None)
        ds.createDimension(Nset_name, nset_num)

        time_var = ds.createVariable('time', 'f4', ('time',))
        time_var.units = f'days since {dates[0]}'
        time_var.calendar = 'standard'
        dates_val = date2num(dates, time_var.units, time_var.calendar)
        time_var[:] = dates_val

        sheds_var = ds.createVariable(Nset_name, 'i4', (Nset_name,))
        sheds_var.units = ''
        sheds_var.long_name = f'{Nset_name} id of element'
        sheds_var[:] = Nset

        ds.institution = 'The Water Problems Institute of the Russian Academy of Sciences'
        ds.source = 'ECOMAG NGMS 2024 v1'

        for var_name in config.vars_long_names:
            if (var_name in data[dts_str]):
                nc_var = ds.createVariable(var_name, 'f4', ('time', Nset_name,), compression='zlib',
                                           least_significant_digit=4)
                # nc_var.units = 'm3 s-1'
                if var_name in config.vars_long_names:
                    nc_var.long_name = config.vars_long_names[var_name]
                else:
                    nc_var.long_name = var_name

                if var_name in config.vars_units:
                    nc_var.units = config.vars_units[var_name]
                else:
                    nc_var.units = var_name

                arr_lst = list(data[dts_str][var_name].values())
                arr = np.vstack(arr_lst)
                nc_var[:] = arr

        ds.close()
