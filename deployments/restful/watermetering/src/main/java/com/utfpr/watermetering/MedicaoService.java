package com.utfpr.watermetering;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class MedicaoService {

    @Autowired
    private MedicaoRepository medicaoRepository;

    public Medicao salvarMedicao(Medicao medicao) {
        return medicaoRepository.save(medicao);
    }

    public Optional<Medicao> obterUltimaMedicaoPorMatricula(String matricula) {
        return medicaoRepository.findTopByMatriculaOrderByDataHoraDesc(matricula);
    }
}

