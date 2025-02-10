import os
import subprocess
import sys

# Configurações de ataque
MODBUS_PORT = 502

# Diretório para armazenar os logs
LOG_DIR = "/logs"
os.makedirs(LOG_DIR, exist_ok=True)

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 metasploit_attack.py <TARGET_IP>")
        sys.exit(1)
    target_ip = sys.argv[1]
    run_metasploit_modbus_attack(target_ip)

