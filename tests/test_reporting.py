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
    assert "frontier_a" in summary["disturbance_by_habitat"]
    assert summary["disturbance_summaries"]


def test_disturbance_recovery_summary_handles_runs_without_disturbance() -> None:
    result = run_simulation(SimulationConfig())
    summary = summarize_disturbance_recovery(result, recolonization_window=8)
    assert summary["disturbance_count"] == 0
    assert summary["disturbance_status_counts"] == {}
    assert isinstance(summary["final_empty_habitats"], list)
