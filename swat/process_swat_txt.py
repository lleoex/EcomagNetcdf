import sys
from pathlib import Path

import pandas as pd

# paths_config.py лежит в корне проекта — добавляем корень в путь поиска модулей
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from paths_config import (
    SWAT_HRU_FILE,
    SWAT_HRU_NC,
    SWAT_RCH_FILE,
    SWAT_RCH_NC,
    SWAT_START_DATE,
    SWAT_SUB_FILE,
    SWAT_SUB_NC,
)


def save_netcdf(
    df: pd.DataFrame,
    output_path: str,
    start_date: str,
    object_field: str,
    csv_path: str | None = None,
) -> None:
    """
    Измерения: object_field и valid_date.
    valid_date — число дней с start_date.
    Записи каждого объекта должны иежедневно и хронологическидти .
    """
    data = df.copy()
    start = pd.Timestamp(start_date).normalize()

    # Поиск столбца без учёта регистра: "hru" найдёт "HRU"
    matches = [
        column for column in data.columns
        if column.lower() == object_field.lower()
    ]
    if len(matches) != 1:
        raise ValueError(f"Не удалось однозначно найти поле {object_field!r}")

    source_field = matches[0]

    if data[source_field].isna().any():
        raise ValueError(f"В поле {source_field!r} есть пропуски")

    if object_field.lower() == "valid_date" or "valid_date" in data.columns:
        raise ValueError("Имя valid_date занято")

    data = data.rename(columns={source_field: object_field})

    data["valid_date"] = (
        data.groupby(object_field, sort=False)
        .cumcount()
        .astype("int32")
    )

    ds = data.set_index([object_field, "valid_date"]).to_xarray()
    ds = ds.transpose(object_field, "valid_date")

    ds["valid_date"].attrs.update({
        "units": f"days since {start:%Y-%m-%d} 00:00:00",
        "calendar": "proleptic_gregorian",
        "standard_name": "time",
        "axis": "T",
    })

    ds.to_netcdf(
        output_path,
        engine="netcdf4",
        encoding={
            "valid_date": {"dtype": "int32", "_FillValue": None},
        },
    )

    data["date"] = (
        start + pd.to_timedelta(data["valid_date"], unit="D")
    ).dt.strftime("%Y-%m-%d")

    if csv_path is None:
        csv_path = str(Path(output_path).with_suffix(".csv"))

    # Идентификатор и даты — первые столбцы
    first_columns = [object_field, "valid_date", "date"]
    other_columns = [
        column for column in data.columns
        if column not in first_columns
    ]

    data[first_columns + other_columns].to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig",
    )
    

def read_swat(file_path:str):
   

    df = pd.read_csv(
        file_path,
        sep=r"\s+",
        skiprows=8,
        dtype={"GIS": str},  # Сохраняем ведущие нули
        encoding="utf-8",
    )
    return df




hru = read_swat(str(SWAT_HRU_FILE))
sub = read_swat(str(SWAT_SUB_FILE))
rch = read_swat(str(SWAT_RCH_FILE))

save_netcdf(hru, str(SWAT_HRU_NC), SWAT_START_DATE, "hru")
save_netcdf(sub, str(SWAT_SUB_NC), SWAT_START_DATE, "sub")
save_netcdf(rch, str(SWAT_RCH_NC), SWAT_START_DATE, "rch")

sub = read_swat(str(SWAT_SUB_FILE))
rch = read_swat(str(SWAT_RCH_FILE))

print(hru)

