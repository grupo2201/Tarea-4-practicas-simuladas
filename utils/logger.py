from datetime import datetime

def log_info(msg):
    with open("logs.txt", "a") as f:
        f.write(f"[INFO] {datetime.now()} - {msg}\n")

def log_error(msg):
    with open("logs.txt", "a") as f:
        f.write(f"[ERROR] {datetime.now()} - {msg}\n")