# Use uma imagem base oficial do Kali Linux
FROM kalilinux/kali-rolling

# Atualize e instale as ferramentas necessárias
RUN apt-get update && \
    apt-get install -y nmap metasploit-framework burpsuite python3 python3-pip hping3

# Instale a biblioteca de ataque DDoS em Python
RUN pip3 install scapy

# Crie um diretório para logs
RUN mkdir /logs

# Copie os scripts de ataque para o contêiner
COPY scripts/ /root/scripts/

# Defina o ponto de entrada para o contêiner
#CMD ["sh", "-c", "echo 'Use the appropriate script to perform an attack (nmap_scan.py, metasploit_attack.py, ddos_attack.py)'"]