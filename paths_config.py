"""
Единая конфигурация путей проекта EcomagNetcdf.

Здесь собраны все абсолютные пути, которые раньше были «зашиты» в отдельных
скриптах (`main.py`, `geopack.py`, `painter.py`, `fore.py`, `foreY.py`,
`swat/process_swat_txt.py`). Чтобы перенести проект на другую машину,
достаточно изменить значения ниже — остальной код трогать не нужно.

Все значения — объекты `pathlib.Path` (кроме дат и прочих не-путей).
"""

from pathlib import Path

# Корень репозитория (каталог, в котором лежит этот файл)
PROJECT_ROOT = Path(__file__).resolve().parent

# =========================================================================
# main.py — конвертация бинарных результатов ECOMAG в NetCDF
# =========================================================================
# Каталог с двоичными файлами модели (аргумент 1 командной строки).
# Ранее в коде встречались варианты:
#   Linux:   /home/gonchukov-lv/data/emg_binary/SRV_BIN/
#   Windows: c:\usr\data\emg_rnl\amur\
ECOMAG_BINARY_DIR = Path(r"c:\usr\data\emg_rnl\amur")

# Каталог для NetCDF-результатов River_*.nc / Sheds_*.nc (аргумент 2)
ECOMAG_RESULTS_DIR = PROJECT_ROOT / "amur2007"

# =========================================================================
# geopack.py — геопривязка рядов и топология речной сети
# =========================================================================
GEO_DIR = Path(r"C:\usr\data\emg_rnl\geo")

# Полигоны ячеек для присоединения рядов Qrvr
CELLS_GPKG = GEO_DIR / "cells3857.gpkg"

# Топология речной сети (столбцы from / to)
RIVER1_CSV = GEO_DIR / "river1.csv"

# Результат join_data_to_geom()
JOIN_RESULT_GPKG = PROJECT_ROOT / "res3857.gpkg"

# =========================================================================
# painter.py — карты по NetCDF и векторному слою
# =========================================================================
# Активный векторный слой для карт.
# Ранее в коде встречались варианты:
#   C:\usr\data\emg_rnl\geo\Amur_wsds2_wgs84.shp
#   d:\gis\geo\Amur_wsds2_wgs84.shp
#   C:\usr\data\emg_rnl\geo\CllsNetWork_wgs84.shp
#   d:\gis\geo\CllsNetWork_wgs84.shp
#   D:\Users\gonchukov-lv\Documents\Yandex.Disk\gis\SWAT\SHPs\Watershed.shp
#   C:\Users\gonchukov-lv\YandexDisk\gis\SWAT\SHPs\Watershed.shp
PAINTER_SHAPE_FILE = Path(r"C:\Users\gonchukov-lv\YandexDisk\gis\SWAT\SHPs\Reach.shp")

# Исходный NetCDF для карт.
# Ранее в коде встречались варианты:
#   C:\Users\gonchukov-lv\Documents\GitHub\EcomagNetcdf\amur2007\Sheds_20070101.nc
#   c:\Users\gonchukov-lv\Documents\GitHub\EcomagNetcdf\2008-2020_da\River_20080101.nc
PAINTER_NC_FILE = PROJECT_ROOT / "swat" / "output_rch.nc"

# =========================================================================
# fore.py / foreY.py — постобработка прогнозных CSV
# =========================================================================
# Каталог с исходными CSV-выпусками прогнозов
FORECAST_SRC_DIR = Path(r"D:\Users\gonchukov-lv\Documents\GitHub\emg2025\EcoAmur\Archive\001\SimOut")

# Каталог прогнозных матриц (fore.py)
FORECAST_MATRIX_DIR = FORECAST_SRC_DIR / "ForecastMatrices"

# Каталог прогнозных матриц с разбивкой по годам (foreY.py)
FORECAST_MATRIX_BY_YEAR_DIR = FORECAST_SRC_DIR / "ForecastMatricesByYear"

# =========================================================================
# swat/process_swat_txt.py — текстовые выходы SWAT -> NetCDF
# =========================================================================
SWAT_OUTPUT_DIR = Path(r"c:\data\SWAT_Razdol\output")

SWAT_HRU_FILE = SWAT_OUTPUT_DIR / "output.hru"
SWAT_SUB_FILE = SWAT_OUTPUT_DIR / "output.sub"
SWAT_RCH_FILE = SWAT_OUTPUT_DIR / "output.rch"

# Начало модельного периода (первая дата в файлах SWAT)
SWAT_START_DATE = "2011-01-01"

# Куда писать NetCDF-результаты
SWAT_HRU_NC = PROJECT_ROOT / "output_hru.nc"
SWAT_SUB_NC = PROJECT_ROOT / "output_sub.nc"
SWAT_RCH_NC = PROJECT_ROOT / "output_rch.nc"
