FROM eclipse-temurin:17-jdk-alpine


RUN wget https://sourceforge.net/projects/scadabr/files/v1.2/ScadaBR_Setup_Linux.zip
COPY scadabr.zip .
RUN unzip scadabr.zip -d /opt/ 

CMD ["sh", "-c", "cd /opt/scadabr/bin && ./startup.sh && tail -f /opt/scadabr/logs/catalina.out"]
