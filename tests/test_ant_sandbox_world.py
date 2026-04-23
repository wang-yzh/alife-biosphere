from alife_biosphere.ant_sandbox import AntSandboxConfig, initialize_world


def test_ant_sandbox_world_initializes_deterministically() -> None:
    first = initialize_world(AntSandboxConfig())
    second = initialize_world(AntSandboxConfig())
    assert first.width == second.width == 128
    assert first.height == second.height == 96
    assert first.colonies == second.colonies
    assert first.food_patches == second.food_patches
    assert first.ants == second.ants
    assert first.terrain == second.terrain


def test_ant_sandbox_world_contains_nest_food_and_ants() -> None:
    world = initialize_world(AntSandboxConfig())
    assert len(world.colonies) == 3
    assert all(colony.nest.radius > 0 for colony in world.colonies.values())
    assert len(world.food_patches) >= 1
    assert len(world.ants) == 32
    assert world.terrain
    assert any(kind == "rock" for kind in world.terrain.values())
    assert {ant.colony_id for ant in world.ants} == {"wei", "shu", "wu"}
    assert all(0 <= ant.x < world.width and 0 <= ant.y < world.height for ant in world.ants)
