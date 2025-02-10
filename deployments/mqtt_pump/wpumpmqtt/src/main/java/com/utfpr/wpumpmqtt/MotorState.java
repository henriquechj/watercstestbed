package com.utfpr.wpumpmqtt;


import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import java.time.LocalDateTime;

@Entity
public class MotorState {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String location;
    private double pressure;
    private boolean motorOn;
    private LocalDateTime timestamp;

    // Getters and Setters
    public String getLocation() {
        return location;
    }
    public void setLocation(String location) {
        this.location = location;
    }
    public double getPressure() {
        return pressure;
    }
    public void setPressure(double pressure) {
        this.pressure = pressure;
    }
    public boolean isMotorOn() {
        return motorOn;
    }
    public void setMotorOn(boolean motorOn) {
        this.motorOn = motorOn;
    }
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }



}