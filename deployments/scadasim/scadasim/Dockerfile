FROM openjdk:17-jdk-slim
VOLUME /tmp
COPY target/scadasim-0.0.1-SNAPSHOT.jar scadasim.jar
ENTRYPOINT ["java","-jar","/scadasim.jar"]
