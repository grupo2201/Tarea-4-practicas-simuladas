from datetime import datetime

def log_info(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje_formateado = f"[INFO] {timestamp} - {msg}"
    print(mensaje_formateado)
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{mensaje_formateado}\n")

def log_error(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje_formateado = f"[ERROR] {timestamp} - {msg}"
    print(mensaje_formateado)
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{mensaje_formateado}\n")