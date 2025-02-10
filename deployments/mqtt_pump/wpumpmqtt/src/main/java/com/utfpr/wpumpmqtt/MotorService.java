package com.utfpr.wpumpmqtt;

import org.eclipse.paho.client.mqttv3.IMqttMessageListener;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.time.LocalDateTime;
import java.util.concurrent.ConcurrentLinkedQueue;

@Service
public class MotorService {

    private static final String TOPIC = "sensor/pressure";

    @Autowired
    private MqttClient mqttClient;

    @Autowired
    private MotorStateRepository motorStateRepository;

    private boolean motorOn = false;
    private ConcurrentLinkedQueue<MqttMessage> messageQueue = new ConcurrentLinkedQueue<>();

    @PostConstruct
    public void subscribeToTopic() throws MqttException {
        mqttClient.subscribe(TOPIC, new IMqttMessageListener() {
            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                messageQueue.add(message); // Adiciona a mensagem à fila
            }
        });
    }

    @Scheduled(fixedRate = 30000)
    public void processMessages() {
        while (!messageQueue.isEmpty()) {
            MqttMessage message = messageQueue.poll();
            if (message != null) {
                String payload = new String(message.getPayload());
                handleIncomingMessage(payload);
            }
        }
    }

    private void handleIncomingMessage(String payload) {
        // Parse the payload to extract location and pressure
        // Example payload: {"location": "Medidor1", "pressure": 23.45}
        // This is a simple implementation, consider using a JSON library like Jackson for real scenarios
        String[] parts = payload.replace("{", "").replace("}", "").replace("\"", "").split(",");
        String location = parts[0].split(":")[1].trim();
        double pressure = Double.parseDouble(parts[1].split(":")[1].trim());

        if (!location.equals("Medidor1")) {
            return; // Ignore messages not from Medidor1
        }

        if (pressure < 10 && !motorOn) {
            motorOn = true;
        } else if (pressure > 50 && motorOn) {
            motorOn = false;
        }

        MotorState motorState = new MotorState();
        motorState.setLocation(location);
        motorState.setPressure(pressure);
        motorState.setMotorOn(motorOn);
        motorState.setTimestamp(LocalDateTime.now());

        motorStateRepository.save(motorState);
    }
}

