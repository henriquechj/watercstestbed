package com.utfpr.wpumpmqtt;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/motor")
public class MotorController {

    @Autowired
    private MotorStateRepository motorStateRepository;

    @GetMapping("/status")
    public MotorState getMotorStatus() {
        return motorStateRepository.findLatestMotorState();
    }
}
