package com.utfpr.wpumpmqtt;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class MqttApplication {

    public static void main(String[] args) {
        SpringApplication.run(MqttApplication.class, args);
    }
}
