package com.utfpr.watermetering;


import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface MedicaoRepository extends JpaRepository<Medicao, Long> {
    Optional<Medicao> findTopByMatriculaOrderByDataHoraDesc(String matricula);
}
