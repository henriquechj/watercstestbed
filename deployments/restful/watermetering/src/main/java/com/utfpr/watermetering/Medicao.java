package com.utfpr.watermetering;

//import javax.persistence.*;
import jakarta.persistence.Entity;
import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
public class Medicao {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String matricula;
    private LocalDateTime dataHora;
    private double medicaoAtual;

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getMatricula() {
        return matricula;
    }

    public void setMatricula(String matricula) {
        this.matricula = matricula;
    }

    public LocalDateTime getDataHora() {
        return dataHora;
    }

    public void setDataHora(LocalDateTime dataHora) {
        this.dataHora = dataHora;
    }

    public double getMedicaoAtual() {
        return medicaoAtual;
    }

    public void setMedicaoAtual(double medicaoAtual) {
        this.medicaoAtual = medicaoAtual;
    }
}
