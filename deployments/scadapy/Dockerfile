FROM python:3.8-slim

RUN apt-get update \
&& apt-get install -y mbpoll
RUN pip install pyModbusTCP
RUN pip install pymodbus
RUN pip install flask

COPY scada_service.py /scada_service.py
COPY clp_client.py /clp_client.py

ENTRYPOINT ["python", "/scada_service.py"]
