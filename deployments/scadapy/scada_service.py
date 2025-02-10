from flask import Flask, jsonify
from pymodbus.client import ModbusTcpClient
from threading import Thread, Event
from time import sleep
import logging

# Configurações de Logging
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Endereços IP e Portas dos CLPs
CLP1_IP = '172.20.0.3'
CLP2_IP = '172.20.0.4'
CLP3_IP = '172.20.0.5'
CLP_PORT = 502

# Variáveis globais para armazenar os valores dos sensores e atuadores
clp_data = {
    'nivel_barragem': 0,
    'nivel_tanque': 0,
    'pressao_rede': 0,
    'bomba_captacao': False,
    'bomba_distribuicao': False
}

# Evento para parar a thread de monitoramento
stop_event = Event()

def read_register(client, address, count):
    try:
        result = client.read_holding_registers(address, count, unit=1)
        if not result.isError():
            return result.registers
        else:
            logger.error(f"Erro ao ler registro: {result}")
            return [0] * count
    except Exception as e:
        logger.error(f"Exception ao ler registro: {e}")
        return [0] * count

def read_coil(client, address, count):
    try:
        result = client.read_coils(address, count, unit=1)
        if not result.isError():
            return result.bits
        else:
            logger.error(f"Erro ao ler coil: {result}")
            return [False] * count
    except Exception as e:
        logger.error(f"Exception ao ler coil: {e}")
        return [False] * count

def monitor_clps():
    while not stop_event.is_set():
        try:
            # Monitoramento do CLP1
            client1 = ModbusTcpClient(CLP1_IP, port=CLP_PORT)
            client1.connect()
            clp_data['nivel_barragem'] = read_register(client1, 0, 1)[0]
            client1.close()

            # Monitoramento do CLP2
            client2 = ModbusTcpClient(CLP2_IP, port=CLP_PORT)
            client2.connect()
            clp_data['nivel_tanque'] = read_register(client2, 0, 1)[0]
            clp_data['bomba_captacao'] = read_coil(client2, 1, 1)[0]
            client2.close()

            # Monitoramento do CLP3
            client3 = ModbusTcpClient(CLP3_IP, port=CLP_PORT)
            client3.connect()
            clp_data['pressao_rede'] = read_register(client3, 0, 1)[0]
            clp_data['bomba_distribuicao'] = read_coil(client3, 1, 1)[0]
            client3.close()

            logger.info(f"Dados CLP1 - Nivel Barragem: {clp_data['nivel_barragem']}")
            logger.info(f"Dados CLP2 - Nivel Tanque: {clp_data['nivel_tanque']}, Bomba Captação: {clp_data['bomba_captacao']}")
            logger.info(f"Dados CLP3 - Pressão Rede: {clp_data['pressao_rede']}, Bomba Distribuição: {clp_data['bomba_distribuicao']}")
        except Exception as e:
            logger.error(f"Erro ao monitorar CLPs: {e}")

        sleep(30)

@app.route('/clp_data', methods=['GET'])
def get_clp_data():
    return jsonify(clp_data)

if __name__ == '__main__':
    # Inicia a thread de monitoramento dos CLPs
    monitor_thread = Thread(target=monitor_clps)
    monitor_thread.start()

    try:
        # Inicia o servidor Flask
        app.run(host='0.0.0.0', port=8080)
    finally:
        stop_event.set()
        monitor_thread.join()




