from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import randint

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
        if data_type == "co":
            return self._data["co"][address:address + count]
        elif data_type == "di":
            return self._data["di"][address:address + count]
        elif data_type == "ir":
            return self._data["ir"][address:address + count]
        elif data_type == "hr":
            return self._data["hr"][address:address + count]

    def set_values(self, address, values, data_type):
        if data_type == "co":
            self._data["co"][address:address + len(values)] = values
        elif data_type == "di":
            self._data["di"][address:address + len(values)] = values
        elif data_type == "ir":
            self._data["ir"][address:address + len(values)] = values
        elif data_type == "hr":
            self._data["hr"][address:address + len(values)] = values

def run_clp(server_ip, server_port, role):
    data_bank = CLPDataBank()
    server = ModbusServer(host=server_ip, port=server_port, data_bank=data_bank, no_block=True)
    server.start()
    print(f"Simulador de {role} iniciado em {server_ip}:{server_port}")

    try:
        while True:
            if role == "CLP1":
                # Simula o nível da barragem de captação
                level = randint(0, 100)
                data_bank.set_values(0, [level], "hr")
                print(f"Nivel Barragem: {level}")

            elif role == "CLP2":
                # Simula o nível do tanque de tratamento
                level = randint(0, 100)
                data_bank.set_values(0, [level], "hr")
                print(f"Nivel Tanque: {level}")
                
                # Leitura do comando da bomba de captação
                bomba_captacao = data_bank.get_values(1, 1, "co")[0]
                print(f"Bomba de captação: {'Ligada' if bomba_captacao else 'Desligada'}")

            elif role == "CLP3":
                # Simula a pressão da rede
                pressure = randint(0, 100)
                data_bank.set_values(0, [pressure], "hr")
                print(f"Pressao Rede: {pressure}")
                
                # Leitura do comando da bomba de distribuição
                bomba_distribuicao = data_bank.get_values(1, 1, "co")[0]
                print(f"Bomba de distribuição: {'Ligada' if bomba_distribuicao else 'Desligada'}")

            sleep(5)

    except KeyboardInterrupt:
        server.stop()
        print(f"Simulador de {role} parado")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Uso: clp_simulator.py <IP> <PORT> <ROLE>")
        sys.exit(1)
    run_clp(sys.argv[1], int(sys.argv[2]), sys.argv[3])

