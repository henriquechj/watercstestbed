import argparse
from pymodbus.client import ModbusTcpClient

def main():
    # Definir os argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Modbus TCP Client')
    parser.add_argument('--host', type=str, required=True, help='Endereço IP do dispositivo Modbus')
    parser.add_argument('--register', type=int, required=True, help='Endereço do registrador')
    parser.add_argument('--value', type=int, required=True, help='Valor a ser escrito no registrador')
    args = parser.parse_args()

    # Conectando ao dispositivo Modbus
    client = ModbusTcpClient(args.host)

    # Escrevendo no registrador
    result = client.write_register(args.register, args.value)

    # Verificando o resultado
    print(f"Resultado do comando: {result}")

    # Fechando a conexão
    client.close()

if __name__ == "__main__":
    main()






