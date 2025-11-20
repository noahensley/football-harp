from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
FILE_PATH = ROOT / "data/data.txt"
FILE_PATH = FILE_PATH.resolve()

DT_FORMAT = "%Y-%m-%d %H:%M:%S"

with open(FILE_PATH, "r", encoding="utf-8") as fp:
    time_data = fp.readlines()
    start = time_data[0].split(" ")
    start = start[0][1:] + " " + start[1][:-1]
    end = time_data[-1].split(" ")
    end = end[0][1:] + " " + end[1][:-1]
    dt_start = datetime.strptime(start, DT_FORMAT)
    dt_end = datetime.strptime(end, DT_FORMAT)
    print(f"4x batteries powered Pi from {start} to {end}.")
    delta_seconds = (dt_end - dt_start).total_seconds()
    print(f"\tTotal duration: {(delta_seconds / 60 / 60):0.4f} hours.")
