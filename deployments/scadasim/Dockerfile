FROM openjdk:17-jdk-slim
VOLUME /tmp
RUN apt-get update \
&& apt-get install -y mbpoll
COPY scadasim.jar scadasim.jar
ENTRYPOINT ["java","-jar","/scadasim.jar"]
