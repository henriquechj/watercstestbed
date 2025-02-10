import logging
from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import randint

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_level(previous_level):
    # Gera uma variação aleatória entre 1 e 10
    variation = randint(1, 5)
    # Decide se a variação será positiva ou negativa
    if randint(0, 1) == 0:
        new_level = previous_level - variation
    else:
        new_level = previous_level + variation
    # Garante que o nível esteja entre 0 e 100
    new_level = max(0, min(100, new_level))
    return new_level

class CLPDataBank(DataBank):
    def __init__(self):
        super().__init__()
        self._data = {
            "co": [False] * 100,   # coils
            "di": [False] * 100,   # discrete inputs
            "ir": [0] * 100,       # input registers
            "hr": [0] * 100        # holding registers
        }

    def get_values(self, address, count, data_type):
        logger.info(f"Recebendo requisição para leitura: tipo={data_type}, endereço={address + 1}, quantidade={count}")
        if address + count > len(self._data[data_type]):
            raise ValueError("Address out of range")
        
        values = []
        if data_type == "co":
            values = self._data["co"][address:address + count]
        elif data_type == "di":
            values = self._data["di"][address:address + count]
        elif data_type == "ir":
            values = self._data["ir"][address:address + count]
        elif data_type == "hr":
            values = self._data["hr"][address:address + count]
        
        logger.info(f"Enviando dados: {values}")
        return values

    def set_values(self, address, values, data_type):
        logger.info(f"Recebendo requisição para escrita: tipo={data_type}, endereço={address + 1}, valores={values}")
        if address + len(values) > len(self._data[data_type]):
            raise ValueError("Address out of range")
        
        if data_type == "co":
            self._data["co"][address:address + len(values)] = values
        elif data_type == "di":
            self._data["di"][address:address + len(values)] = values
        elif data_type == "ir":
            self._data["ir"][address:address + len(values)] = values
        elif data_type == "hr":
            self._data["hr"][address:address + len(values)] = values
        
        logger.info(f"Dados escritos com sucesso")

def run_clp(server_ip, server_port, role):
    data_bank = CLPDataBank()
    server = ModbusServer(host=server_ip, port=server_port, data_bank=data_bank, no_block=True)
    server.start()
    logger.info(f"Simulador de {role} iniciado em {server_ip}:{server_port}")

    # Inicializa os níveis
    nivel_barragem = 80
    nivel_tanque = 50
    pressao_rede = 10

    try:
        while True:
            if role == "CLP1":
                # Atualiza o nível da barragem de captação
                nivel_barragem = update_level(nivel_barragem)
                data_bank.set_values(0, [nivel_barragem], "hr")
                logger.info(f"Nivel Barragem: {nivel_barragem}")
                # Verificar o valor após definição
                nivel_barragem_lido = data_bank.get_values(0, 1, "hr")
                logger.info(f"Valor do Nivel Barragem após set_values: {nivel_barragem_lido}")

            elif role == "CLP2":
                # Atualiza o nível do tanque de tratamento
                nivel_tanque = update_level(nivel_tanque)
                data_bank.set_values(0, [nivel_tanque], "hr")
                logger.info(f"Nivel Tanque: {nivel_tanque}")
                # Verificar o valor após definição
                nivel_tanque_lido = data_bank.get_values(0, 1, "hr")
                logger.info(f"Valor do Nivel Tanque após set_values: {nivel_tanque_lido}")
                
                # Leitura do comando da bomba de captação
                bomba_captacao = data_bank.get_values(0, 1, "co")[0]
                logger.info(f"Bomba de captação: {'Ligada' if bomba_captacao else 'Desligada'}")

            elif role == "CLP3":
                # Atualiza a pressão da rede
                pressao_rede = update_level(pressao_rede)
                data_bank.set_values(0, [pressao_rede], "hr")
                logger.info(f"Pressao Rede: {pressao_rede}")
                # Verificar o valor após definição
                pressao_rede_lido = data_bank.get_values(0, 1, "hr")
                logger.info(f"Valor da Pressao Rede após set_values: {pressao_rede_lido}")
                
                # Leitura do comando da bomba de distribuição
                bomba_distribuicao = data_bank.get_values(0, 1, "co")[0]
                logger.info(f"Bomba de distribuição: {'Ligada' if bomba_distribuicao else 'Desligada'}")

            sleep(5)

    except KeyboardInterrupt:
        server.stop()
        logger.info(f"Simulador de {role} parado")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        logger.error("Uso: clp_simulator.py <IP> <PORT> <ROLE>")
        sys.exit(1)
    run_clp(sys.argv[1], int(sys.argv[2]), sys.argv[3])

