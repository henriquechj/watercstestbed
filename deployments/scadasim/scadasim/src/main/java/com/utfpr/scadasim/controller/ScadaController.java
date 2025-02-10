package com.utfpr.scadasim.controller;

import com.serotonin.modbus4j.exception.ErrorResponseException;
import com.serotonin.modbus4j.exception.ModbusInitException;
import com.serotonin.modbus4j.exception.ModbusTransportException;
import com.utfpr.scadasim.service.ControlService;

import java.util.HashMap;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.utfpr.scadasim.model.*;;

@RestController
public class ScadaController {

    private final ControlService controlService;

    public ScadaController(ControlService controlService) {
        this.controlService = controlService;
    }

    @GetMapping("/check-and-update")
    public void checkAndUpdate() throws ModbusTransportException, ErrorResponseException, ModbusInitException {
        controlService.checkAndUpdate();
    }

   @GetMapping("/status")
    public Map<String, Object> getStatus() { 
        Map<String, Object> status = new HashMap<>();
        status.put("nivelBarragem", controlService.getNivelBarragem().getValue());
        status.put("nivelTanque", controlService.getNivelTanque().getValue());
        status.put("pressaoRede", controlService.getPressaoRede().getValue());
        status.put("bombaCaptacao", controlService.getBombaCaptacao().isStatus());
        status.put("bombaDistribuicao", controlService.getBombaDistribuicao().isStatus());
        return status;
    } 


}

