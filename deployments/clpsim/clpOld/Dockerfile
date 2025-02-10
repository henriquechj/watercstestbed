FROM python:3.8-slim

RUN pip install pyModbusTCP

COPY clp_simulator.py /clp_simulator.py

ENTRYPOINT ["python", "/clp_simulator.py"]
