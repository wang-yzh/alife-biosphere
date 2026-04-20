from alife_biosphere.config import HABITAT_FAMILIES, HabitatConfig, SimulationConfig, WorldConfig
from alife_biosphere.world import World


def test_config_round_trip_shape() -> None:
    config = SimulationConfig()
    payload = config.to_dict()
    assert payload["world"]["seed"] == 7
    assert len(payload["world"]["habitats"]) == 7
    assert len(payload["world"]["habitat_edges"]) == 7


def test_invalid_habitat_capacity_raises() -> None:
    try:
        HabitatConfig(habitat_id="x", capacity=0)
    except ValueError as exc:
        assert "capacity" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_invalid_habitat_family_raises() -> None:
    try:
        HabitatConfig(habitat_id="x", habitat_family="bogus")
    except ValueError as exc:
        assert "habitat_family" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_default_world_builds_expected_graph() -> None:
    world = World.from_config(WorldConfig())
    assert len(world.habitats) == 7
    assert set(HABITAT_FAMILIES) == {"nursery", "refuge", "frontier", "wild"}
    assert world.habitats["refuge"].neighbors == (
        "frontier_a",
        "frontier_b",
        "nursery_a",
        "nursery_b",
    )


def test_invalid_disturbance_interval_raises() -> None:
    try:
        WorldConfig(disturbance_interval=-1)
    except ValueError as exc:
        assert "disturbance_interval" in str(exc)
    else:
        raise AssertionError("expected ValueError")
