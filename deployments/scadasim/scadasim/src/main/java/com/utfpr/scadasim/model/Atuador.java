package com.utfpr.scadasim.model;

public class Atuador {
    private String name;
    private boolean status;

    public Atuador(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }   
}