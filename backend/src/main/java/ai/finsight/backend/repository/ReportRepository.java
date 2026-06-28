package ai.finsight.backend.repository;

import ai.finsight.backend.model.Report;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ReportRepository extends JpaRepository<Report, Long> {
    List<Report> findByUserIdAndSymbolOrderByGeneratedAtDesc(Long userId, String symbol);

    List<Report> findByUserIdOrderByGeneratedAtDesc(Long userId);

    Optional<Report> findByReportId(String reportId);
}