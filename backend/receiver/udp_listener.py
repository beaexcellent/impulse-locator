import socket
import json
import time
from datetime import datetime
from pathlib import Path

import sys
sys.path.append("/srv/impulse")

from event_queue import event_queue

LOG_DIR = Path("/srv/impulse/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

def log_event(event):
    """Append event JSON to a daily log file."""
    day = datetime.utcnow().strftime("%Y-%m-%d")
    logfile = LOG_DIR / f"events_{day}.log"
    with logfile.open("a") as f:
        f.write(json.dumps(event) + "\n")

def start_udp_listener(host="0.0.0.0", port=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"[receiver] Listening on UDP {host}:{port}")

    while True:
        data, addr = sock.recvfrom(4096)
        try:
            event = json.loads(data.decode())
            event["received_at"] = time.time()
            log_event(event)
            event_queue.put(event)
            print("[receiver] Event:", event)
        except Exception as e:
            print("[receiver] Bad packet:", e)

if __name__ == "__main__":
    start_udp_listener()