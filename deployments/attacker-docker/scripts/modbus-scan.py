import argparse
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException

def read_registers(client, start_address, count):
    try:
        # Ler múltiplos registradores
        response = client.read_holding_registers(start_address, count)
        if not isinstance(response, ModbusIOException):
            print(f"Registradores lidos a partir do endereço {start_address}: {response.registers}")
        else:
            print(f"Erro na leitura dos registradores a partir do endereço {start_address}")
    except Exception as e:
        print(f"Erro: {e}")

def write_register(client, address, value):
    try:
        # Escrever em um registrador específico
        result = client.write_register(address, value)
        if not isinstance(result, ModbusIOException):
            print(f"Registrador {address} escrito com o valor {value}")
        else:
            print(f"Erro ao escrever no registrador {address}")
    except Exception as e:
        print(f"Erro: {e}")

def main():
    parser = argparse.ArgumentParser(description="Modbus TCP Scanner")
    parser.add_argument('--host', type=str, required=True, help="Endereço IP do dispositivo Modbus")
    parser.add_argument('--port', type=int, default=502, help="Porta TCP do dispositivo Modbus (padrão 502)")
    parser.add_argument('--start', type=int, default=0, help="Endereço inicial dos registradores para leitura")
    parser.add_argument('--count', type=int, default=10, help="Número de registradores para ler")
    parser.add_argument('--write_address', type=int, help="Endereço do registrador para escrita")
    parser.add_argument('--write_value', type=int, help="Valor a ser escrito no registrador")
    args = parser.parse_args()

    # Conectar ao dispositivo Modbus
    client = ModbusTcpClient(args.host, port=args.port)

    if client.connect():
        print(f"Conectado ao dispositivo Modbus {args.host}:{args.port}")
        
        # Leitura de registradores
        read_registers(client, args.start, args.count)

        # Escrever em um registrador, se especificado
        if args.write_address is not None and args.write_value is not None:
            write_register(client, args.write_address, args.write_value)

        # Fechar a conexão
        client.close()
        print("Conexão encerrada.")
    else:
        print(f"Não foi possível conectar ao dispositivo {args.host}:{args.port}")

if __name__ == "__main__":
    main()


