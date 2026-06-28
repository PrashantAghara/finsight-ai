package ai.finsight.backend.repository;

import ai.finsight.backend.model.Alert;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface AlertRepository extends JpaRepository<Alert, UUID> {
    List<Alert> findByUserId(Long userId);

    List<Alert> findByUserIdAndSymbol(Long userId, String symbol);

    List<Alert> findByUserIdAndStatus(Long userId, String status);

    List<Alert> findBySymbolAndStatus(String symbol, String status);
}