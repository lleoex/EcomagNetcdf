import datetime
import netCDF4 as nc
import numpy as np
from datetime import datetime
from cftime import num2date, date2num

def CreatePixelNcFile(pixel_data: dict[str: dict[str : dict[int:np.ndarray]]]):
    for dts_str in pixel_data:
        if len(pixel_data[dts_str]) == 2:
            qlat = pixel_data[dts_str]['Qlat']
            qrvr = pixel_data[dts_str]['Qrvr']
            
            if len(qlat) == len(qrvr):
                dates = []
                for dt in qlat:
                    if dt in qrvr:
                        y = dt//10000
                        m = (dt//100)%100
                        dd = dt%100
                        d = datetime(y, m,dd)
                        dates.append(d)
                    else:
                        print(f'dates are different in qlat and qrvr')
                
                
                


                pix_num = len(next(iter(qlat.values())))
                ds = nc.Dataset(f'Disharge_{dts_str}.nc','w', format='NETCDF4')
                ds.createDimension('time', None)
                
                ds.createDimension('pixels', pix_num)

                time_var = ds.createVariable('time','f8',('time',))
                time_var.units = f'days since {dates[0]}'
                time_var.calendar = 'standard'
                dates_val = date2num(dates,time_var.units , time_var.calendar )
                
                print(ds)
            else:
                print(f'qlat and qrvr have different dates lendht at dts={dts_str}')