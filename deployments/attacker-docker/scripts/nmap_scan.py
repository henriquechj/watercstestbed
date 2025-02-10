import os
import subprocess
import sys

# Diretório para armazenar os logs
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)

def run_nmap(target):
    """Executa uma varredura Nmap no alvo especificado e salva o log."""
    log_file = os.path.join(LOG_DIR, f"nmap_{target}.log")
    print(f"Executando Nmap em {target}...")
    with open(log_file, 'w') as f:
        subprocess.run(["nmap", "-sV", target], stdout=f, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 nmap_scan.py <TARGET_IP>")
        sys.exit(1)
    target_ip = sys.argv[1]
    run_nmap(target_ip)

