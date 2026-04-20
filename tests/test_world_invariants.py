from alife_biosphere.config import SimulationConfig
from alife_biosphere.simulation import run_simulation


def test_resources_and_integrity_stay_bounded() -> None:
    result = run_simulation(SimulationConfig())
    for habitat in result.world.habitats.values():
        assert habitat.resource_level >= 0.0
        assert habitat.resource_level <= habitat.max_resource_level
        assert -1.0 <= habitat.climate_state <= 1.0
        assert habitat.occupancy_pressure >= 0.0
        assert habitat.depletion_trace >= 0.0
        assert habitat.disturbance_trace >= 0.0
    for organism in result.world.organisms.values():
        assert 0.0 <= organism.integrity <= 1.0
        assert organism.life_stage in {"juvenile", "mature", "senescent", "dead"}
        assert organism.generation >= 0
        if not organism.alive:
            assert organism.integrity == 0.0
            assert organism.death_reason is not None
