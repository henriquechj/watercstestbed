package com.utfpr.wpressmqtt;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.Random;

@Service
public class SensorService {

    private static final String TOPIC = "sensor/pressure";

    @Autowired
    private MqttClient mqttClient;

    private final Random random = new Random();

    @Scheduled(fixedRate = 30000)
    public void sendSensorData() {
        String location = "Medidor1";
        double pressure = 0 + (60 - 0) * random.nextDouble();

        String payload = String.format("{\"location\": \"%s\", \"pressure\": %.2f}", location, pressure);
        MqttMessage message = new MqttMessage(payload.getBytes());
        message.setQos(1);

        try {
            mqttClient.publish(TOPIC, message);
            System.out.println("Message published: " + payload);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }
}
