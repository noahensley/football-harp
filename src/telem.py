from pathlib import Path
import os
import time
from datetime import datetime

ROOT_DIR = Path(__file__).parent.parent
TELEM_DIR = ROOT_DIR / "./data"
LOG_FNAME = TELEM_DIR / "data.txt"
LOG_FNAME = LOG_FNAME.resolve()

def log_data(data, file=LOG_FNAME):
    try:
        print("[TELEM] Logging telemetry data...", end="")
        with open(file, "a+", encoding="utf-8") as fp:
            if os.path.getsize(file) > 0:
                fp.write("\n")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bytes = fp.write(f"[{timestamp}] {data}")
    except Exception as e:
    	raise
    print(f"DONE ({bytes} bytes logged)") 
    return bytes
