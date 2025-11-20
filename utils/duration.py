from datetime import datetime

dt_format = "%Y-%m-%d %H:%M:%S"

with open("power_log.txt", "r", encoding="utf-8") as fp:
    time_data = fp.readlines()
    start = time_data[0].rstrip()[1:-1]
    end = time_data[-1].rstrip()[1:-1]
    dt_start = datetime.strptime(start, dt_format)
    dt_end = datetime.strptime(end, dt_format)
    print(f"4x batteries powered Pi from {start} to {end}.")
    delta_seconds = (dt_end - dt_start).total_seconds()
    print(f"\tTotal duration: {(delta_seconds / 60 / 60):0.4f} hours.")
