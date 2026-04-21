from alife_biosphere.config import SimulationConfig
from alife_biosphere.simulation import run_simulation


def test_resources_and_integrity_stay_bounded() -> None:
    result = run_simulation(SimulationConfig())
    for habitat in result.world.habitats.values():
        assert habitat.resource_level >= 0.0
        assert habitat.resource_level <= habitat.max_resource_level
        assert -1.0 <= habitat.climate_state <= 1.0
        assert 0.0 <= habitat.hazard_level <= 1.0
        assert habitat.regeneration_rate >= 0.0
        assert habitat.occupancy_pressure >= 0.0
        assert habitat.depletion_trace >= 0.0
        assert habitat.disturbance_trace >= 0.0
        assert 0.0 <= habitat.memory_field <= 1.0
        assert habitat.recovery_lag >= 0
        assert habitat.empty_ticks >= 0
    for organism in result.world.organisms.values():
        assert 0.0 <= organism.integrity <= 1.0
        assert organism.life_stage in {"juvenile", "mature", "senescent", "dead"}
        assert organism.generation >= 0
        if not organism.alive:
            assert organism.integrity == 0.0
            assert organism.death_reason is not None


def test_habitat_history_changes_regeneration_or_hazard() -> None:
    result = run_simulation(SimulationConfig())
    assert any(habitat.memory_field > 0.0 for habitat in result.world.habitats.values())
    assert any(
        abs(habitat.regeneration_rate - habitat.base_regeneration_rate) > 1e-6
        or abs(habitat.hazard_level - habitat.base_hazard_level) > 1e-6
        for habitat in result.world.habitats.values()
    )
