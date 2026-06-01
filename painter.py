import os.path
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
import netCDF4
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Press the green button in the gutter to run the script.
config = {
    # "SoilFrstDep": {
    #     "vmin": 0,
    #     "vmax": 400,
    #     "title": "Глубина промерзания, см",
    #     "cmap": "cool",
    #     "mult": 0.1
    #
    # },
    # "SoilMoist": {
    #     "vmin": 0.3,
    #     "vmax": 1.2,
    #     #"title": "Влажность почвы, доля FC",
    #     "title": "",
    #     "cmap": "RdBu"
    #  },
    #    "Qrvr": {
    #      "vmin": 0,
    #       "vmax": 1,
    #       "title": "",
    #       "cmap": "cool"
    #   },
    #
    #
    # # "SnHgt": {
    #     "vmin": 0,
    #     "vmax": 200,
    #     "title": "Высота снежного покрова, см",
    #     "cmap": "PuBu"
    # },
    #
    # "SnWE": {
    #     "vmin": 0,
    #     "vmax": 300,
    #     #"title": "Влагозапас снега, мм",
    #     "title": "",
    #     "cmap": "PuBuGn"
    # },
    # "ESUM": {
    #     "vmin": 0,
    #     "vmax": 10,
    #     "title": "Суммарное испарение, мм/сут",
    #     "cmap": "PuBu"
    # },
    "Pcp": {
        "vmin": 0,
         "vmax": 150,
         #"title": "Сумма осадков, мм/5сут",
         "title":"",
         "cmap": "PuBuGn"
     },
    #
    # "Tair": {
    #     "vmin": -40,
    #     "vmax": 40,
    #     "title": "T, град С",
    #     "cmap": "jet"
    # }
}

if __name__ == '__main__':
    shp_file = 'C:\\usr\\data\\emg_rnl\\geo\\Amur_wsds2_wgs84.shp'
    #shp_file = 'C:\\usr\\data\\emg_rnl\\geo\\CllsNetWork_wgs84.shp'
    nc_file = 'C:\\Users\\gonchukov-lv\\Documents\\GitHub\\EcomagNetcdf\\amur2007\\Sheds_20070101.nc'
    #nc_file = 'c:\\Users\\gonchukov-lv\\Documents\\GitHub\\EcomagNetcdf\\2008-2020_da\\River_20080101.nc'
    dst_dir = 'amur2008_river'  # sys.argv[3]

    #shp_file = sys.argv[1]
    #nc_file = sys.argv[2]
    #dst_dir = sys.argv[3]
    brief = False

    if brief:
        dst_dir += '_briefly'

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    # os.mkdir(dst_dir)
    gpd_shp = gpd.read_file((shp_file))
    nc = netCDF4.Dataset(nc_file)
    time_var = nc['time']
    time_arr = netCDF4.num2date(time_var[:], time_var.units)
    watersheds_arr = nc['watersheds'][:]
    #watersheds_arr = nc['pixels'][:]
    for vname in config:
        # vname = 'SoilMoist'
        if vname not in nc.variables:
            continue

        if not os.path.exists(os.path.join(dst_dir, vname)):
            os.makedirs(os.path.join(dst_dir, vname))
        # os.mkdir(os.path.join(dst_dir,vname))

        mult = 1
        if "mult" in config[vname]:
            mult = config[vname]["mult"]

        #data_src = nc[vname][:] * mult
        #avg_cell_value = np.max(data_src,axis=0)
        #data = data_src / avg_cell_value

        data = nc[vname][:] * mult


        for t in range(len(time_arr)):
            #if (brief and time_arr[t].day == 15 and time_arr[t].month in [2,8]) or (not brief and time_arr[t].day in [5,15,25]) :
            if (brief and time_arr[t].day == 15 and time_arr[t].month in [2, 8]) or (
                    not brief
                    #and time_arr[t].year in [2013]
                    #and time_arr[t].month in [10,5]
                   and time_arr[t].day in [5,10,15,20,25,30]
            ):
                df = pd.DataFrame(np.vstack((watersheds_arr,
                                             #data[t,:]
                                             #np.average(data[t-5:t, :],axis=0)
                                             np.sum(data[t - 5:t, :], axis=0)
                                             )), index=['gridcode', 'value']).transpose()
                #df = pd.DataFrame(np.vstack((watersheds_arr, data[t, :])), index=['CllId', 'value']).transpose()

                gdf = gpd.GeoDataFrame(df.merge(gpd_shp, on="gridcode"))
                #gdf = gpd.GeoDataFrame(df.merge(gpd_shp, on="CllId"))
                if brief:
                    w,h = 4, 3
                else:
                    w, h = 15, 12
                margin = 0.2

                fig_file = os.path.join(dst_dir, vname, f'{time_arr[t]:%Y%m%d}.png')
                fig, ax = plt.subplots( figsize=(w, h))
                ax.set_axis_off()

                if brief:
                    fig.suptitle(f'{time_arr[t]:%Y}', y=0.96)
                else:
                    fig.suptitle(f'{config[vname]["title"]}\n{time_arr[t]:%Y-%m-%d}', y=0.8, x=0.2,fontsize='xx-large' )
                # divider = make_axes_locatable(ax)
                # cax = divider.append_axes("bottom", size="5%", pad=0.3)


                gdf.plot(ax=ax,
                         column='value',
                         cmap=config[vname]["cmap"],
                         #
                         #legend=not brief,
                         #linewidth=gdf['ShtrlOrd']-1,
                         # cax=cax,
                         legend_kwds={"orientation": "horizontal", "fraction": 0.05},
                         vmin=config[vname]["vmin"],
                         vmax=config[vname]["vmax"],
                         # vmax = 100
                         )  # , scheme='quantiles')

                fig.savefig(fig_file, bbox_inches='tight', pad_inches=0.1)
                plt.close(fig)
                print(f'{vname} {time_arr[t]}')

    hi = 0xfff << 1
    print(f'{hi=}')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
