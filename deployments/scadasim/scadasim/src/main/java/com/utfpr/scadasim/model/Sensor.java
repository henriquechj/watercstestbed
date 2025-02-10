package com.utfpr.scadasim.model;

public class Sensor {
    private String name;
    private double value;

    public Sensor(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }
}
