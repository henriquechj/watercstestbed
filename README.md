# Water Cyber Security Testbed: Arquitetura Conteinerizada para Plataforma de Testes em Sistemas Industriais de Água

Este repositório contém o código-fonte para a implementação da arquitetura de plataforma de testes proposta na dissertação de mestrado "Arquitetura Conteinerizada para Plataforma de Testes: Coleta de Dados de Atividades Maliciosas em Sistemas Industriais de Água" e no artigo "Containerized Testbed Architecture for Cybersecurity Data Collection on Malicious Activities in Industrial Water Systems".

O objetivo deste projeto é fornecer uma plataforma de testes modular, de baixo custo e de código aberto para simular um sistema industrial de tratamento e distribuição de água. A plataforma permite a simulação de ataques cibernéticos em um ambiente isolado para avaliar medidas de segurança e coletar dados para pesquisas em cibersegurança.

## Visão Geral da Arquitetura

A arquitetura utiliza contêineres Docker para simular os componentes de um sistema de controle industrial (ICS) de uma instalação de tratamento e distribuição de água, estruturada de acordo com o modelo de referência Purdue. Ela integra tecnologias de Indústria 4.0, como dispositivos IoT e protocolos como MQTT e HTTP, com componentes tradicionais de ICS, como CLPs e sistemas SCADA, que se comunicam via Modbus TCP.

A plataforma é dividida em três subprocessos que simulam as etapas de captação, tratamento e distribuição da água:
* **SP1 (Captação e Tratamento):** Simula a medição do nível da barragem e o bombeamento para o tanque de tratamento. Utiliza três contêineres para simular CLPs que controlam sensores e atuadores via Modbus TCP.
* **SP2 (Distribuição Intermediária):** Simula um sensor de pressão e um pressurizador controlados por dispositivos IoT. A comunicação é feita através de um broker MQTT.
* **SP3 (Distribuição Final):** Simula um hidrômetro digital (IoT) que envia dados de consumo para um serviço web RESTful via requisições HTTP POST.

Todos os dados são centralizados em um sistema SCADA (ScadaBR), que oferece uma interface humano-máquina (HMI) para a visualização e controle da operação.

![Arquitetura da Plataforma de Testes](https://github.com/henriquechj/watercstestbed/raw/main/images/arquitetura.png)


## Coleta de Dados

A coleta de dados é um componente central da arquitetura e é realizada utilizando a pilha **ELK (Elasticsearch, Logstash, Kibana)** e agentes **Beats**.
* **Packetbeat:** Captura pacotes de rede para análise de tráfego.
* **Metricbeat:** Coleta métricas de utilização de recursos como CPU, memória e disco dos contêineres.
* **Filebeat:** Monitora e coleta logs gerados pelas aplicações e pelos ataques simulados.

Os dados coletados são processados pelo Logstash, armazenados no Elasticsearch e podem ser visualizados através de dashboards no Kibana.

## Cenário de Ataques

A plataforma inclui um contêiner baseado em Kali Linux para simular um atacante, permitindo a execução de diversos cenários de ataque baseados no framework MITRE ATT&CK para ICS. Os ataques simulados nos experimentos incluem:

1.  **Reconhecimento:** Varredura da rede com `Nmap` para identificar dispositivos ativos, portas abertas e serviços em execução.
2.  **Ataque de Negação de Serviço Distribuído (DDoS):** Utilização do `hping3` para enviar um grande volume de pacotes TCP, com o objetivo de sobrecarregar os recursos dos dispositivos e interromper os serviços.
3.  **Ataque a Serviços Web:** Uso da ferramenta `Nikto` para escanear os serviços HTTP em busca de vulnerabilidades como a falta de cabeçalhos de segurança, métodos HTTP inseguros (PUT/DELETE) e exposição de interfaces de gerenciamento.
4.  **Injeção de Comando Remoto no Modbus:** Exploração da falta de autenticação do protocolo Modbus TCP para ler e escrever diretamente nos registradores dos CLPs usando um script Python, alterando o comportamento do processo físico.

## Pré-requisitos

* **Sistema Operacional:** Linux (testado em Fedora 39).
* **Docker:** Versão 27.1.1 ou superior.
* **Docker Compose:** Versão 1.29.2 ou superior.

## Como Executar

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/henriquechj/watercstestbed.git](https://github.com/henriquechj/watercstestbed.git)
    cd watercstestbed
    ```

2.  Inicie todos os contêineres da simulação e da plataforma de coleta de dados usando o Docker Compose:
    ```bash
    docker-compose up -d
    ```

3.  Acesse as interfaces dos serviços:
    * **SCADABR (SCADA System):** `http://localhost:8080` (A porta pode variar dependendo do mapeamento no `docker-compose.yaml`). É necessário configurar as fontes de dados (Data Sources) para conectar aos CLPs (Modbus), ao broker MQTT e ao serviço RESTful, conforme descrito na seção 4.1 da dissertação.
    * **Kibana (Visualização de Dados):** `http://localhost:5601`.
    * **Serviço RESTful (API de medições):** `http://localhost:8082` (A porta pode variar).

4.  Para executar os cenários de ataque, acesse o shell do contêiner do atacante:
    ```bash
    docker exec -it attacker /bin/bash
    ```
    Dentro do contêiner, você encontrará os scripts e ferramentas (Nmap, Hping3, Nikto) para realizar os ataques contra os serviços nas redes `scadanet` (172.20.0.0/16) e `cloud` (172.19.0.0/16).

## Citação

Se você utilizar esta plataforma em sua pesquisa, por favor, cite os seguintes trabalhos:

* **Artigo:**
    Jorge, C. H., Nacamura Jr, L., & Vendramin, A. C. B. K. (2025). Containerized Testbed Architecture for Cybersecurity Data Collection on Malicious Activities in Industrial Water Systems. Journal of the Brazilian Computer Society, 31(1), 613–628. https://doi.org/10.5753/jbcs.2025.5358  

* **Dissertação de Mestrado:**
    JORGE, Carlos Henrique. Arquitetura conteinerizada para plataforma de testes: coleta de dados de atividades maliciosas em sistemas industriais de água. 2025. Dissertação (Mestrado em Computação Aplicada) - Universidade Tecnológica Federal do Paraná, Curitiba, 2025. https://riut.utfpr.edu.br/jspui/handle/1/36691
