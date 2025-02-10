from pymodbus.client import ModbusTcpClient
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def read_holding_registers(ip, port, start_address, count):
    client = ModbusTcpClient(ip, port)
    connection = client.connect()
    if connection:
        response = client.read_holding_registers(start_address, count, unit=1)
        if not response.isError():
            print(f"Read Holding Registers: {response.registers}")
        else:
            print("Error reading holding registers")
        client.close()
    else:
        print("Unable to connect to Modbus server")

if __name__ == "__main__":
    read_holding_registers("172.20.0.3", 502, 0, 10)