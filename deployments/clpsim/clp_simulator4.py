import logging
from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import randint

# Define endereços de registro como constantes para melhor manutenção
NIVEL_BARRAGEM_ADDRESS = 0
NIVEL_TANQUE_ADDRESS = 0
BOMBA_CAPTACAO_ADDRESS = 1  # Supondo que esses endereços são conhecidos
PRESSAO_REDE_ADDRESS = 0
BOMBA_DISTRIBUICAO_ADDRESS = 1

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Função para atualizar o nível com uma variação aleatória
def update_level(previous_level):
    variation = randint(1, 10)
    new_level = previous_level + variation if randint(0, 1) else previous_level - variation
    return max(0, min(99, new_level))

class CLPDataBank(DataBank):
    """Classe personalizada de banco de dados para o simulador CLP."""

    def __init__(self):
        super().__init__()
        self.coils = [False] * 100
        self.discrete_inputs = [False] * 100
        self.input_registers = [0] * 100
        self.holding_registers = [0] * 100

    def get_coils(self, address, count):
        return self._get_values(self.coils, address, count, 'coils')

    def get_discrete_inputs(self, address, count):
        return self._get_values(self.discrete_inputs, address, count, 'discrete inputs')

    def get_input_registers(self, address, count):
        return self._get_values(self.input_registers, address, count, 'input registers')

    def get_holding_registers(self, address, count):
        return self._get_values(self.holding_registers, address, count, 'holding registers')

    def set_coils(self, address, values):
        self._set_values(self.coils, address, values, 'coils')

    def set_discrete_inputs(self, address, values):
        self._set_values(self.discrete_inputs, address, values, 'discrete inputs')

    def set_input_registers(self, address, values):
        self._set_values(self.input_registers, address, values, 'input registers')

    def set_holding_registers(self, address, values):
        self._set_values(self.holding_registers, address, values, 'holding registers')

    def _get_values(self, storage, address, count, type_name):
        logger.debug(f"Recebendo requisição para leitura: tipo={type_name}, endereço={address}, quantidade={count}")
        if address + count > len(storage):
            raise ValueError("Endereço fora do intervalo")
        values = storage[address:address + count]
        logger.debug(f"Enviando dados: {values}")
        return values

    def _set_values(self, storage, address, values, type_name):
        logger.debug(f"Recebendo requisição para escrita: tipo={type_name}, endereço={address}, valores={values}")
        if address + len(values) > len(storage):
            raise ValueError("Endereço fora do intervalo")
        storage[address:address + len(values)] = values
        logger.debug(f"Dados escritos com sucesso: {storage[address:address + len(values)]}")

def run_clp(server_ip, server_port, role, update_interval=5):
    """Inicia o simulador CLP.

    Args:
        server_ip (str): Endereço IP do servidor.
        server_port (int): Número da porta do servidor.
        role (str): Função do CLP (ex: "CLP1", "CLP2", "CLP3").
        update_interval (int, opcional): Intervalo (em segundos) entre as atualizações. Default é 5.
    """

    data_bank = CLPDataBank()
    server = ModbusServer(host=server_ip, port=server_port, data_bank=data_bank, no_block=True)
    server.start()
    logger.info(f"Simulador de {role} iniciado em {server_ip}:{server_port}")

    # Inicializa os níveis
    nivel_barragem = 80
    nivel_tanque = 50
    pressao_rede = 10
    bomba_ligada = False  # Supondo estado inicial

    try:
        while True:
            if role == "CLP1":
                nivel_barragem = update_level(nivel_barragem)
                data_bank.set_holding_registers(NIVEL_BARRAGEM_ADDRESS, [nivel_barragem])
                logger.info(f"Nivel Barragem atualizado para: {nivel_barragem}")
            elif role == "CLP2":
                nivel_tanque = update_level(nivel_tanque)
                data_bank.set_holding_registers(NIVEL_TANQUE_ADDRESS, [nivel_tanque])
                logger.info(f"Nivel Tanque atualizado para: {nivel_tanque}")
                bomba_ligada = data_bank.get_coils(BOMBA_CAPTACAO_ADDRESS, 1)[0]
                logger.info(f"Bomba de captação: {'Ligada' if bomba_ligada else 'Desligada'}")
            elif role == "CLP3":
                pressao_rede = update_level(pressao_rede)
                data_bank.set_holding_registers(PRESSAO_REDE_ADDRESS, [pressao_rede])
                logger.info(f"Pressao Rede atualizada para: {pressao_rede}")

                # Controla a bomba de distribuição com base na pressão da rede (exemplo de lógica)
                bomba_distribuicao = pressao_rede < 50  # Liga a bomba se a pressão estiver baixa
                data_bank.set_coils(BOMBA_DISTRIBUICAO_ADDRESS, [bomba_distribuicao])
                logger.info(f"Bomba de distribuição: {'Ligada' if bomba_distribuicao else 'Desligada'}")

            sleep(update_interval)
    except KeyboardInterrupt:
        server.stop()
        logger.info(f"Simulador de {role} parado")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        logger.error("Uso: clp_simulator2.py <IP> <PORT> <ROLE>")
        sys.exit(1)
    run_clp(sys.argv[1], int(sys.argv[2]), sys.argv[3])


