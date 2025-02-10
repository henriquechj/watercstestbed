package com.utfpr.wpumpmqtt;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface MotorStateRepository extends JpaRepository<MotorState, Long> {

    
    @Query(value = "SELECT * FROM motor_state ORDER BY timestamp DESC LIMIT 1", nativeQuery = true)
    MotorState findLatestMotorState();

}

