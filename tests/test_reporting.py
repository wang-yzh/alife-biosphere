from alife_biosphere.config import SimulationConfig, WorldConfig
from alife_biosphere.reporting import summarize_disturbance_recovery
from alife_biosphere.simulation import run_simulation


def test_disturbance_recovery_summary_tracks_collapses_and_recovery() -> None:
    result = run_simulation(
        SimulationConfig(
            world=WorldConfig(
                ticks=40,
                founder_count=10,
                disturbance_interval=8,
                disturbance_resource_shock=2.0,
                disturbance_hazard_pulse=0.12,
                senescence_age=24,
                max_age=50,
            )
        )
    )
    summary = summarize_disturbance_recovery(result, recolonization_window=8)
    assert summary["disturbance_count"] == 5
    assert summary["collapse_count"] > 0
    assert summary["recolonization_count"] > 0
    assert summary["disturbance_status_counts"]["collapsed_and_recovered"] >= 1
    assert sum(summary["disturbance_status_counts"].values()) == summary["disturbance_count"]
    assert summary["lineage_recovery_mode_counts"]
    assert summary["recovery_source_mode_counts"]
    assert summary["recovery_source_habitat_counts"]
    assert summary["recovery_source_family_counts"]
    assert "frontier_a" in summary["disturbance_by_habitat"]
    assert summary["disturbance_summaries"]
    assert any(
        item["lineage_recovery_mode"] in {"same_lineage_return", "replacement_recovery", "mixed_recovery"}
        for item in summary["disturbance_summaries"]
        if item["lineage_recovery_mode"] is not None
    )
    assert any(
        item["recovery_source_mode"] in {"single_habitat_source", "multi_habitat_source"}
        for item in summary["disturbance_summaries"]
        if item["recovery_source_mode"] is not None
    )
    assert any(item["source_habitats"] for item in summary["disturbance_summaries"])


def test_disturbance_recovery_summary_handles_runs_without_disturbance() -> None:
    result = run_simulation(SimulationConfig())
    summary = summarize_disturbance_recovery(result, recolonization_window=8)
    assert summary["disturbance_count"] == 0
    assert summary["disturbance_status_counts"] == {}
    assert summary["lineage_recovery_mode_counts"] == {}
    assert summary["recovery_source_habitat_counts"] == {}
    assert summary["recovery_source_family_counts"] == {}
    assert summary["recovery_source_mode_counts"] == {}
    assert isinstance(summary["final_empty_habitats"], list)
