from pathlib import Path
import pandas as pd
import re

src_dir = Path(r"D:\Users\gonchukov-lv\Documents\GitHub\emg2025\EcoAmur\Archive\001\SimOut")          # каталог с исходными CSV
out_dir = Path(r"D:\Users\gonchukov-lv\Documents\GitHub\emg2025\EcoAmur\Archive\001\SimOut\ForecastMatrices")
out_dir.mkdir(exist_ok=True)

csv_files = sorted(src_dir.glob("*.csv"))

# Читаем каждый файл только один раз
data = []
sites = set()

for file in csv_files:

    df = pd.read_csv(file)

    # берем только последние 8 строк
    last8 = df.iloc[-8:]

    data.append(last8)

    for col in df.columns:
        m = re.match(r"^(\d+)_Qm$", col)
        if m:
            sites.add(m.group(1))

sites = sorted(sites)

print(f"Found {len(csv_files)} files")
print(f"Found {len(sites)} sites")

for site in sites:

    qm = f"{site}_Qm"
    qs = f"{site}_Qs"

    rows = {}

    for df in data:

        if qm not in df.columns or qs not in df.columns:
            continue

        values = df[["Date", qm, qs]].to_numpy()

        for lead in range(8):

            dt = values[lead][0]
            obs = values[lead][1]
            fcst = values[lead][2]

            if dt not in rows:
                rows[dt] = {
                    "Date": dt,
                    "Obs": obs
                }

            rows[dt][f"F{lead}"] = fcst

    result = pd.DataFrame(rows.values())
    result.sort_values("Date", inplace=True)

    columns = ["Date", "Obs"] + [f"F{i}" for i in range(8)]

    for col in columns:
        if col not in result.columns:
            result[col] = None

    result = result[columns]

    result.to_csv(
        out_dir / f"{site}_forecast_matrix.csv",
        index=False
    )

    print(f"{site} done")

print("Finished")