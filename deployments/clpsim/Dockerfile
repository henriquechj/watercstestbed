FROM python:3.8-slim

RUN pip install pyModbusTCP
RUN pip install pymodbus

COPY clp_simulator3.py /clp_simulator.py
COPY clp_client.py /clp_client.py

ENTRYPOINT ["python", "/clp_simulator.py"]
