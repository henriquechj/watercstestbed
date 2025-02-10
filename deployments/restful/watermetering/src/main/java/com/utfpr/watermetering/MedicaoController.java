package com.utfpr.watermetering;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/api/medicoes")
public class MedicaoController {

    @Autowired
    private MedicaoService medicaoService;

    @PostMapping
    public ResponseEntity<Medicao> registrarMedicao(@RequestBody Medicao medicao) {
        Medicao novaMedicao = medicaoService.salvarMedicao(medicao);
        return ResponseEntity.ok(novaMedicao);
    }

    @GetMapping("/ultima/{matricula}")
    public ResponseEntity<Medicao> obterUltimaMedicao(@PathVariable String matricula) {
        Optional<Medicao> medicao = medicaoService.obterUltimaMedicaoPorMatricula(matricula);
        return medicao.map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }
}
