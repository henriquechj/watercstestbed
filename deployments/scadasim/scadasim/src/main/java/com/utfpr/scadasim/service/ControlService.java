package com.utfpr.scadasim.service;

import com.utfpr.scadasim.model.Atuador;
import com.utfpr.scadasim.model.Sensor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class ControlService {
    private static final Logger logger = LoggerFactory.getLogger(ControlService.class);

    private final ModbusService modbusService;
    private final Sensor nivelBarragem;
    private final Sensor nivelTanque;
    private final Sensor pressaoRede;
    private final Atuador bombaCaptacao;
    private final Atuador bombaDistribuicao;

    public ControlService(ModbusService modbusService) {
        this.modbusService = modbusService;
        this.nivelBarragem = new Sensor("Nivel Barragem");
        this.nivelTanque = new Sensor("Nivel Tanque");
        this.pressaoRede = new Sensor("Pressao Rede");
        this.bombaCaptacao = new Atuador("Bomba Captacao");
        this.bombaDistribuicao = new Atuador("Bomba Distribuicao");
    }

    public void checkAndUpdate() {
        // Simulação da leitura dos sensores e controle dos atuadores

        // CLP1: Verificar o nível da barragem de captação
        nivelBarragem.setValue(readSensorValue("172.20.0.3", 502, 0));
        logger.info("Nivel Barragem0: {}", nivelBarragem.getValue());

        nivelBarragem.setValue(readSensorValue("172.20.0.3", 502, 1));
        logger.info("Nivel Barragem1: {}", nivelBarragem.getValue());

        nivelBarragem.setValue(readSensorValue("172.20.0.3", 502, 2));
        logger.info("Nivel Barragem2: {}", nivelBarragem.getValue());

        // CLP2: Verificar o nível do tanque de tratamento
        nivelTanque.setValue(readSensorValue("172.20.0.4", 502, 0));
        logger.info("Nivel Tanque: {}", nivelTanque.getValue());
        if (nivelTanque.getValue() < 50) {
            bombaCaptacao.setStatus(true);
        } else if (nivelTanque.getValue() >= 100) {
            bombaCaptacao.setStatus(false);
        }
        writeActuatorValue("172.20.0.4", 502, 1, bombaCaptacao.isStatus());
        logger.info("Bomba Captacao: {}", bombaCaptacao.isStatus());

        // CLP3: Verificar a pressão da rede
        pressaoRede.setValue(readSensorValue("172.20.0.5", 502, 0));
        logger.info("Pressão Rede: {}", pressaoRede.getValue());
        if (pressaoRede.getValue() < 40) {
            bombaDistribuicao.setStatus(true);
        } else if (pressaoRede.getValue() > 80) {
            bombaDistribuicao.setStatus(false);
        }
        writeActuatorValue("172.20.0.5", 502, 1, bombaDistribuicao.isStatus());
        logger.info("Bomba Distribuicao: {}", bombaDistribuicao.isStatus());
    }

    private double readSensorValue(String ip, int port, int offset) {
        try {
            short[] result = modbusService.readHoldingRegisters(ip, port, offset, 1);
            return result != null ? result[0] : 0.0;
        } catch (Exception e) {
            logger.error("Erro ao ler sensor", e);
            return 0.0;
        }
    }

    private void writeActuatorValue(String ip, int port, int offset, boolean value) {
        try {
            modbusService.writeCoil(ip, port, 1, offset, value);
        } catch (Exception e) {
            logger.error("Erro ao escrever atuador", e);
        }
    }

    public Sensor getNivelBarragem() {
        return nivelBarragem;
    }

    public Sensor getNivelTanque() {
        return nivelTanque;
    }

    public Sensor getPressaoRede() {
        return pressaoRede;
    }

    public Atuador getBombaCaptacao() {
        return bombaCaptacao;
    }

    public Atuador getBombaDistribuicao() {
        return bombaDistribuicao;
    }
}


