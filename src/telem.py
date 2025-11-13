from pathlib import Path
import os

ROOT_DIR = Path(__file__).parent.parent
TELEM_DIR = ROOT_DIR / "./data"
LOG_FNAME = TELEM_DIR / "data.txt"

def log_data(data, file=LOG_FNAME):
    try:
        print("[TELEM] Logging telemetry data...", end="")
        with open(file, "a+", encoding="utf-8") as fp:
            if os.path.getsize(file) > 0:
                fp.write("\n")
            bytes = fp.write(data)
    except Exception as e:
    	raise
    print(f"DONE ({bytes} bytes logged)") 
    return bytes
