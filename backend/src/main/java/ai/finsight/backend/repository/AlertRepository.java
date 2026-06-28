package ai.finsight.backend.repository;

import ai.finsight.backend.model.Alert;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AlertRepository extends JpaRepository<Alert, Long> {
    List<Alert> findByUserId(Long userId);

    List<Alert> findByUserIdAndSymbol(Long userId, String symbol);

    List<Alert> findByUserIdAndStatus(Long userId, String status);

    List<Alert> findBySymbolAndStatus(String symbol, String status);
}