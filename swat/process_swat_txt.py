import pandas as pd


def save_netcdf(
    df: pd.DataFrame,
    output_path: str,
    start_date: str,
    object_field: str,
) -> None:
    """
    Измерения: object_field и valid_date.
    valid_date — число дней с start_date.
    Записи каждого объекта должны идти ежедневно и хронологически.
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

def read_swat(file_path:str):
   

    df = pd.read_csv(
        file_path,
        sep=r"\s+",
        skiprows=8,
        dtype={"GIS": str},  # Сохраняем ведущие нули
        encoding="utf-8",
    )
    return df




hru_file = "D:\\data\\SWAT_Razdol\\output\\output.hru"
sub_file = "D:\\data\\SWAT_Razdol\\output\\output.sub"
rch_file = "D:\\data\\SWAT_Razdol\\output\\output.rch"

hru = read_swat(hru_file)
sub = read_swat(sub_file)
rch = read_swat(rch_file)

save_netcdf(hru, "output_hru.nc", "2011-01-01", "hru")
save_netcdf(sub, "output_sub.nc", "2011-01-01", "sub")
save_netcdf(rch, "output_rch.nc", "2011-01-01", "rch")

sub = read_swat(sub_file)
rch = read_swat(rch_file)

print(hru)

