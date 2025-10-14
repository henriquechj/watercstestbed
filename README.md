# Water Cyber Security Testbed: Arquitetura Conteinerizada para Plataforma de Testes em Sistemas Industriais de Água

[cite_start]Este repositório contém o código-fonte para a implementação da arquitetura de plataforma de testes proposta na dissertação de mestrado "Arquitetura Conteinerizada para Plataforma de Testes: Coleta de Dados de Atividades Maliciosas em Sistemas Industriais de Água" [cite: 852, 853, 857, 858] [cite_start]e no artigo "Containerized Testbed Architecture for Cybersecurity Data Collection on Malicious Activities in Industrial Water Systems"[cite: 2].

[cite_start]O objetivo deste projeto é fornecer uma plataforma de testes modular, de baixo custo e de código aberto para simular um sistema industrial de tratamento e distribuição de água[cite: 230, 1449]. [cite_start]A plataforma permite a simulação de ataques cibernéticos em um ambiente isolado para avaliar medidas de segurança e coletar dados para pesquisas em cibersegurança[cite: 986, 1451].

## Visão Geral da Arquitetura

[cite_start]A arquitetura utiliza contêineres Docker para simular os componentes de um sistema de controle industrial (ICS) de uma instalação de tratamento e distribuição de água, estruturada de acordo com o modelo de referência Purdue[cite: 13, 901, 1512]. [cite_start]Ela integra tecnologias de Indústria 4.0, como dispositivos IoT e protocolos como MQTT e HTTP, com componentes tradicionais de ICS, como CLPs e sistemas SCADA, que se comunicam via Modbus TCP[cite: 230, 231, 236, 1450].

[cite_start]A plataforma é dividida em três subprocessos que simulam as etapas de captação, tratamento e distribuição da água[cite: 277, 1556]:
* [cite_start]**SP1 (Captação e Tratamento):** Simula a medição do nível da barragem e o bombeamento para o tanque de tratamento[cite: 280, 282, 1558]. [cite_start]Utiliza três contêineres para simular CLPs que controlam sensores e atuadores via Modbus TCP[cite: 284, 1570].
* [cite_start]**SP2 (Distribuição Intermediária):** Simula um sensor de pressão e um pressurizador controlados por dispositivos IoT[cite: 307, 1596]. [cite_start]A comunicação é feita através de um broker MQTT[cite: 308, 1597].
* [cite_start]**SP3 (Distribuição Final):** Simula um hidrômetro digital (IoT) que envia dados de consumo para um serviço web RESTful via requisições HTTP POST[cite: 313, 314, 1603, 1604].

[cite_start]Todos os dados são centralizados em um sistema SCADA (ScadaBR), que oferece uma interface humano-máquina (HMI) para a visualização e controle da operação[cite: 468, 471, 1606, 1607, 1731].

![Arquitetura da Plataforma de Testes](https://github.com/henriquechj/watercstestbed/raw/main/images/arquitetura.png)
[cite_start]*(Adaptação da Figura 3 do artigo e Figura 8 da dissertação [cite: 268, 1520])*

## Coleta de Dados

[cite_start]A coleta de dados é um componente central da arquitetura e é realizada utilizando a pilha **ELK (Elasticsearch, Logstash, Kibana)** e agentes **Beats**[cite: 337, 1631, 1632].
* [cite_start]**Packetbeat:** Captura pacotes de rede para análise de tráfego[cite: 340, 1634].
* [cite_start]**Metricbeat:** Coleta métricas de utilização de recursos como CPU, memória e disco dos contêineres[cite: 341, 1636].
* [cite_start]**Filebeat:** Monitora e coleta logs gerados pelas aplicações e pelos ataques simulados[cite: 341, 1635].

[cite_start]Os dados coletados são processados pelo Logstash, armazenados no Elasticsearch e podem ser visualizados através de dashboards no Kibana[cite: 343, 344, 345, 1637, 1638].

## Cenário de Ataques

[cite_start]A plataforma inclui um contêiner baseado em Kali Linux para simular um atacante, permitindo a execução de diversos cenários de ataque baseados no framework MITRE ATT&CK para ICS[cite: 319, 320, 1609, 1610]. Os ataques simulados nos experimentos incluem:

1.  [cite_start]**Reconhecimento:** Varredura da rede com `Nmap` para identificar dispositivos ativos, portas abertas e serviços em execução[cite: 322, 1613].
2.  [cite_start]**Ataque de Negação de Serviço Distribuído (DDoS):** Utilização do `hping3` para enviar um grande volume de pacotes TCP, com o objetivo de sobrecarregar os recursos dos dispositivos e interromper os serviços[cite: 325, 326, 1619, 1620].
3.  [cite_start]**Ataque a Serviços Web:** Uso da ferramenta `Nikto` para escanear os serviços HTTP em busca de vulnerabilidades como a falta de cabeçalhos de segurança, métodos HTTP inseguros (PUT/DELETE) e exposição de interfaces de gerenciamento[cite: 631, 633, 635, 1945, 1948, 1958].
4.  [cite_start]**Injeção de Comando Remoto no Modbus:** Exploração da falta de autenticação do protocolo Modbus TCP para ler e escrever diretamente nos registradores dos CLPs usando um script Python, alterando o comportamento do processo físico[cite: 640, 642, 1964, 1966].

## Pré-requisitos

* [cite_start]**Sistema Operacional:** Linux (testado em Fedora 39)[cite: 376, 1673].
* [cite_start]**Docker:** Versão 27.1.1 ou superior[cite: 376, 1673].
* [cite_start]**Docker Compose:** Versão 1.29.2 ou superior[cite: 378, 1674].

## Como Executar

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/henriquechj/watercstestbed.git](https://github.com/henriquechj/watercstestbed.git)
    cd watercstestbed
    ```

2.  [cite_start]Inicie todos os contêineres da simulação e da plataforma de coleta de dados usando o Docker Compose[cite: 378, 1674]:
    ```bash
    docker-compose up -d
    ```

3.  Acesse as interfaces dos serviços:
    * [cite_start]**SCADABR (SCADA System):** `http://localhost:8080` (A porta pode variar dependendo do mapeamento no `docker-compose.yaml`)[cite: 419, 1681]. [cite_start]É necessário configurar as fontes de dados (Data Sources) para conectar aos CLPs (Modbus), ao broker MQTT e ao serviço RESTful, conforme descrito na seção 4.1 da dissertação[cite: 1736].
    * [cite_start]**Kibana (Visualização de Dados):** `http://localhost:5601`[cite: 420, 1689].
    * [cite_start]**Serviço RESTful (API de medições):** `http://localhost:8082` (A porta pode variar)[cite: 419, 1681].

4.  [cite_start]Para executar os cenários de ataque, acesse o shell do contêiner do atacante[cite: 480, 1808]:
    ```bash
    docker exec -it attacker /bin/bash
    ```
    [cite_start]Dentro do contêiner, você encontrará os scripts e ferramentas (Nmap, Hping3, Nikto) para realizar os ataques contra os serviços nas redes `scadanet` (172.20.0.0/16) e `cloud` (172.19.0.0/16)[cite: 499, 1813].

## Citação

Se você utilizar esta plataforma em sua pesquisa, por favor, cite os seguintes trabalhos:

* **Artigo:**
    Jorge, C. H., Nacamura Jr, L., & Vendramin, A. C. B. K. (2025). Containerized Testbed Architecture for Cybersecurity Data Collection on Malicious Activities in Industrial Water Systems. [cite_start]*Journal of the Brazilian Computer Society*, 31(1). https://doi.org/10.5753/jbes.2025.5358 [cite: 1, 3, 6, 7, 10]

* **Dissertação de Mestrado:**
    Jorge, C. H. (2025). *Arquitetura Conteinerizada para Plataforma de Testes: Coleta de Dados de Atividades Maliciosas em Sistemas Industriais de Água*. [cite_start]Dissertação de Mestrado, Universidade Tecnológica Federal do Paraná. https://riut.utfpr.edu.br/jspui/handle/1/36691 [cite: 852, 856, 861, 872, 876]
