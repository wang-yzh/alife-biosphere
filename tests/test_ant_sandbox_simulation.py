from alife_biosphere.ant_sandbox import (
    AntAgentConfig,
    AntSandboxConfig,
    ColonyConfig,
    FoodPatchConfig,
    initialize_world,
    NestConfig,
    TerrainConfig,
    build_showcase_config,
)
from alife_biosphere.ant_sandbox.reporting import summarize_behavior_roles
from alife_biosphere.ant_sandbox.simulation import _choose_step, run_simulation
from alife_biosphere.ant_sandbox.validation import summarize_validation_status, ValidationCase


def test_ant_sandbox_run_is_deterministic() -> None:
    first = run_simulation(AntSandboxConfig())
    second = run_simulation(AntSandboxConfig())
    assert first.summary() == second.summary()
    assert [event.to_dict() for event in first.events] == [event.to_dict() for event in second.events]


def test_ant_sandbox_produces_foraging_loop_events() -> None:
    result = run_simulation(AntSandboxConfig())
    event_types = {event.event_type for event in result.events}
    assert "food_pickup" in event_types
    assert "food_unload" in event_types
    assert "nest_feed" in event_types
    assert sum(1 for event in result.events if event.event_type == "food_unload") > 0


def test_default_showcase_uses_multiple_food_sources() -> None:
    result = run_simulation(AntSandboxConfig(ticks=240))
    pickup_counts: dict[str, int] = {}
    for event in result.events:
        if event.event_type != "food_pickup" or event.habitat_id is None:
            continue
        pickup_counts[event.habitat_id] = pickup_counts.get(event.habitat_id, 0) + 1
    active_sources = [patch_id for patch_id, count in pickup_counts.items() if count >= 5]
    assert len(active_sources) >= 2


def test_ant_sandbox_keeps_ants_in_bounds() -> None:
    result = run_simulation(AntSandboxConfig())
    assert all(0 <= ant.x < result.world.width and 0 <= ant.y < result.world.height for ant in result.world.ants)


def test_ant_sandbox_with_pheromones_beats_no_pheromones() -> None:
    cfg_on = AntSandboxConfig(
        width=64,
        height=48,
        nest=NestConfig(x=16, y=24, radius=3, initial_stored_food=18, colony_upkeep_per_ant_tick=0.0),
        food_patches=(
            FoodPatchConfig("food_a", x=46, y=14, radius=4, amount=72, max_amount=72, regrowth_rate=0, respawn_delay_ticks=18),
        ),
        terrain=TerrainConfig(enabled=True),
        ants=AntAgentConfig(
            food_sense_radius=6,
            pheromone_enabled=True,
            pheromone_sense_radius=10,
            trail_deposit=2.0,
            trail_decay=0.02,
            hunger_return_threshold=5.0,
            nest_feed_amount=4.0,
        )
    )
    cfg_off = AntSandboxConfig(
        width=64,
        height=48,
        nest=NestConfig(x=16, y=24, radius=3, initial_stored_food=18, colony_upkeep_per_ant_tick=0.0),
        food_patches=(
            FoodPatchConfig("food_a", x=46, y=14, radius=4, amount=72, max_amount=72, regrowth_rate=0, respawn_delay_ticks=18),
        ),
        terrain=TerrainConfig(enabled=True),
        ants=AntAgentConfig(
            food_sense_radius=6,
            pheromone_enabled=False,
            pheromone_sense_radius=10,
            trail_deposit=2.0,
            trail_decay=0.02,
            hunger_return_threshold=5.0,
            nest_feed_amount=4.0,
        )
    )
    with_pheromones = run_simulation(cfg_on)
    without_pheromones = run_simulation(cfg_off)
    on_unloads = sum(1 for event in with_pheromones.events if event.event_type == "food_unload")
    off_unloads = sum(1 for event in without_pheromones.events if event.event_type == "food_unload")
    assert on_unloads >= off_unloads
    assert sum(1 for event in with_pheromones.events if event.event_type == "trail_deposit") > 0
    assert sum(1 for event in without_pheromones.events if event.event_type == "trail_deposit") == 0


def test_ant_sandbox_can_show_births_and_deaths_in_longer_run() -> None:
    result = run_simulation(
        AntSandboxConfig(
            ticks=420,
            colonies=(),
            nest=NestConfig(initial_stored_food=240, colony_upkeep_per_ant_tick=0.0),
            food_patches=(
                FoodPatchConfig(
                    "food_a",
                    x=38,
                    y=14,
                    radius=3,
                    amount=120,
                    max_amount=120,
                    regrowth_rate=1,
                    relocate_on_depletion=False,
                ),
                FoodPatchConfig(
                    "food_b",
                    x=48,
                    y=35,
                    radius=4,
                    amount=180,
                    max_amount=180,
                    regrowth_rate=1,
                    relocate_on_depletion=False,
                ),
            ),
            ants=AntAgentConfig(
                max_age=260,
                max_population=44,
                spawn_food_cost=1,
                spawn_interval=6,
                pheromone_enabled=True,
                hunger_return_threshold=5.0,
                nest_feed_amount=4.0,
            ),
        )
    )
    event_types = {event.event_type for event in result.events}
    assert "ant_birth" in event_types
    assert "ant_death" in event_types
    summaries = [event.payload for event in result.events if event.event_type == "tick_summary"]
    alive_counts = [summary["alive"] for summary in summaries]
    assert min(alive_counts) > 0
    assert max(alive_counts) <= 44


def test_ant_sandbox_role_summary_produces_multiple_clusters() -> None:
    config = AntSandboxConfig(
        ticks=420,
        colonies=(),
        nest=NestConfig(initial_stored_food=240, colony_upkeep_per_ant_tick=0.0),
        food_patches=(
            FoodPatchConfig(
                "food_a",
                x=38,
                y=14,
                radius=3,
                amount=120,
                max_amount=120,
                regrowth_rate=1,
                relocate_on_depletion=False,
            ),
            FoodPatchConfig(
                "food_b",
                x=48,
                y=35,
                radius=4,
                amount=180,
                max_amount=180,
                regrowth_rate=1,
                relocate_on_depletion=False,
            ),
        ),
        ants=AntAgentConfig(
            max_age=200,
            max_population=44,
            spawn_food_cost=3,
            spawn_interval=6,
            pheromone_enabled=True,
        ),
    )
    result = run_simulation(config)
    summary = summarize_behavior_roles(config, result, cluster_count=3)
    assert summary["cluster_summaries"]
    assert len(summary["cluster_summaries"]) == 3
    assert sum(cluster["member_count"] for cluster in summary["cluster_summaries"]) == len(summary["per_ant"])
    assert len(summary["role_distribution"]) >= 2


def test_hungry_ants_can_refuel_at_nest() -> None:
    config = AntSandboxConfig(
        ticks=80,
        colonies=(),
        nest=AntSandboxConfig().nest.__class__(initial_stored_food=20),
        ants=AntAgentConfig(
            initial_energy=5.0,
            max_energy=20.0,
            metabolism_cost=0.04,
            hunger_return_threshold=8.0,
            nest_feed_amount=5.0,
        ),
    )
    result = run_simulation(config)
    feed_events = [event for event in result.events if event.event_type == "nest_feed"]
    assert feed_events
    assert all(event.payload["energy"] > 5.0 for event in feed_events)


def test_colony_upkeep_consumes_nest_food() -> None:
    config = AntSandboxConfig(
        ticks=6,
        colonies=(),
        nest=NestConfig(initial_stored_food=12, colony_upkeep_per_ant_tick=0.6),
        ants=AntAgentConfig(
            ant_count=1,
            max_population=1,
            initial_energy=20.0,
            max_energy=20.0,
            metabolism_cost=0.01,
            hunger_return_threshold=0.0,
            pheromone_enabled=False,
        ),
    )
    result = run_simulation(config)
    upkeep_events = [event for event in result.events if event.event_type == "nest_upkeep"]
    assert upkeep_events
    assert result.world.nest.stored_food < 12


def test_food_source_contention_events_can_emerge() -> None:
    config = AntSandboxConfig(
        ticks=120,
        width=64,
        height=48,
        colonies=(),
        nest=NestConfig(x=16, y=24, radius=3, initial_stored_food=12, colony_upkeep_per_ant_tick=0.0),
        food_patches=(
            FoodPatchConfig("food_a", x=32, y=24, radius=4, amount=28, max_amount=28, regrowth_rate=0, respawn_delay_ticks=18),
            FoodPatchConfig("food_b", x=47, y=16, radius=3, amount=20, max_amount=20, regrowth_rate=0, respawn_delay_ticks=18),
        ),
        terrain=TerrainConfig(enabled=False),
        ants=AntAgentConfig(
            ant_count=24,
            max_population=24,
            food_sense_radius=18,
            pheromone_enabled=True,
            pheromone_sense_radius=12,
            trail_deposit=1.8,
            trail_decay=0.02,
            hunger_return_threshold=5.0,
            nest_feed_amount=4.0,
        ),
    )
    result = run_simulation(config)
    contested_events = [event for event in result.events if event.event_type == "food_source_contested"]
    assert contested_events
    assert any(patch.competition_pressure > 0 for patch in result.world.food_patches)


def test_non_carrying_ants_switch_to_much_better_visible_food() -> None:
    config = AntSandboxConfig(
        ticks=1,
        width=64,
        height=48,
        colonies=(),
        nest=NestConfig(x=12, y=24, radius=3, initial_stored_food=0, colony_upkeep_per_ant_tick=0.0),
        food_patches=(
            FoodPatchConfig("stale_far", x=56, y=40, radius=3, amount=10, max_amount=10, value_score=0.7),
            FoodPatchConfig("rich_near", x=28, y=24, radius=4, amount=80, max_amount=80, value_score=1.8),
        ),
        terrain=TerrainConfig(enabled=False),
        ants=AntAgentConfig(
            ant_count=1,
            max_population=1,
            food_sense_radius=12,
            pheromone_enabled=False,
            hunger_return_threshold=0.0,
            initial_energy=18.0,
            max_energy=20.0,
        ),
    )
    world = initialize_world(config)
    ant = world.ants[0]
    ant.x = 26
    ant.y = 24
    ant.target_patch_id = "stale_far"
    world.occupied_cells = {(ant.x, ant.y)}

    _choose_step(world, ant, config, tick=1)

    assert ant.target_patch_id == "rich_near"


def test_depleted_food_patch_reseeds_to_new_site() -> None:
    config = AntSandboxConfig(
        ticks=24,
        width=64,
        height=48,
        colonies=(),
        nest=NestConfig(x=16, y=24, radius=3, initial_stored_food=0, colony_upkeep_per_ant_tick=0.0),
        food_patches=(
            FoodPatchConfig(
                "food_a",
                x=18,
                y=24,
                radius=1,
                amount=1,
                max_amount=5,
                regrowth_rate=0,
                respawn_delay_ticks=4,
            ),
        ),
        terrain=TerrainConfig(enabled=False),
        ants=AntAgentConfig(
            ant_count=1,
            max_population=1,
            initial_energy=20.0,
            max_energy=20.0,
            metabolism_cost=0.01,
            hunger_return_threshold=0.0,
            pheromone_enabled=False,
            food_sense_radius=18,
        ),
    )
    result = run_simulation(config)
    reseed_events = [event for event in result.events if event.event_type == "food_patch_reseed"]
    assert reseed_events
    event = reseed_events[0]
    assert (event.payload["from_x"], event.payload["from_y"]) != (event.payload["to_x"], event.payload["to_y"])


def test_depleted_food_patch_can_regrow_in_place_after_delay() -> None:
    config = AntSandboxConfig(
        ticks=20,
        width=64,
        height=48,
        colonies=(),
        nest=NestConfig(x=16, y=24, radius=3, initial_stored_food=0, colony_upkeep_per_ant_tick=0.0),
        food_patches=(
            FoodPatchConfig(
                "food_a",
                x=18,
                y=24,
                radius=1,
                amount=1,
                max_amount=5,
                regrowth_rate=2,
                relocate_on_depletion=False,
                respawn_delay_ticks=4,
                regrow_only_when_empty=True,
            ),
        ),
        terrain=TerrainConfig(enabled=False),
        ants=AntAgentConfig(
            ant_count=1,
            max_population=1,
            initial_energy=20.0,
            max_energy=20.0,
            metabolism_cost=0.01,
            hunger_return_threshold=0.0,
            pheromone_enabled=False,
            food_sense_radius=18,
        ),
    )
    result = run_simulation(config)
    regrow_events = [event for event in result.events if event.event_type == "food_patch_regrow"]
    assert regrow_events
    event = regrow_events[0]
    assert (event.payload["x"], event.payload["y"]) == (18, 24)


def test_showcase_config_disables_births_and_extends_lifespan() -> None:
    config = build_showcase_config(ticks=240)
    assert config.ants.allow_spawning is False
    assert config.ants.max_age > config.ticks


def test_combat_freezes_both_ants_until_resolution() -> None:
    config = AntSandboxConfig(
        ticks=12,
        width=48,
        height=32,
        colonies=(
            ColonyConfig(
                colony_id="wei",
                display_name="Wei",
                color="#375a7f",
                ant_count=1,
                nest=NestConfig(x=16, y=16, radius=2, initial_stored_food=0, colony_upkeep_per_ant_tick=0.0),
            ),
            ColonyConfig(
                colony_id="shu",
                display_name="Shu",
                color="#b24a3a",
                ant_count=1,
                nest=NestConfig(x=19, y=16, radius=2, initial_stored_food=0, colony_upkeep_per_ant_tick=0.0),
            ),
        ),
        food_patches=(
            FoodPatchConfig("food_a", x=40, y=16, radius=2, amount=20, max_amount=20, regrowth_rate=0, relocate_on_depletion=False),
        ),
        terrain=TerrainConfig(enabled=False),
        ants=AntAgentConfig(
            ant_count=2,
            max_population=2,
            pheromone_enabled=False,
            metabolism_cost=0.01,
            food_sense_radius=6,
            combat_enabled=True,
            combat_radius=3,
            combat_duration=4,
            combat_cooldown=2,
            combat_decision_threshold=0.0,
        ),
    )
    result = run_simulation(config)
    combat_start = next(event for event in result.events if event.event_type == "combat_start")
    combat_end = next(event for event in result.events if event.event_type == "combat_end")
    engaged_ids = {combat_start.payload["ant_a"], combat_start.payload["ant_b"]}
    moves_during_combat = [
        event
        for event in result.events
        if event.event_type == "move"
        and event.organism_id in engaged_ids
        and combat_start.tick <= event.tick <= combat_end.tick
    ]
    assert not moves_during_combat


def test_validation_status_evaluates_expected_metric_states() -> None:
    cases = [
        ValidationCase(
            seed=7,
            base_unloads=10,
            pheromone_on_unloads=10,
            pheromone_off_unloads=7,
            persistence_births=5,
            persistence_deaths=36,
            persistence_alive_min=1,
            persistence_alive_max=36,
            role_label_count=2,
            disturbance_recovery_ratio=3.0,
        ),
        ValidationCase(
            seed=11,
            base_unloads=11,
            pheromone_on_unloads=12,
            pheromone_off_unloads=8,
            persistence_births=4,
            persistence_deaths=30,
            persistence_alive_min=2,
            persistence_alive_max=35,
            role_label_count=2,
            disturbance_recovery_ratio=2.5,
        ),
    ]
    summary = summarize_validation_status(cases)
    assert summary["metric_status"]["M2_foraging_loop"] == "pass"
    assert summary["metric_status"]["M3_pheromone_effectiveness"] == "pass"
    assert summary["metric_status"]["M4_colony_persistence"] == "pass"
    assert summary["metric_status"]["M5_role_differentiation"] == "pass"
    assert summary["metric_status"]["M6_disturbance_recovery"] == "pass"


def test_ant_sandbox_disturbance_keeps_some_function_after_shock() -> None:
    result = run_simulation(
        AntSandboxConfig(
            ticks=300,
            colonies=(),
            nest=NestConfig(initial_stored_food=240, colony_upkeep_per_ant_tick=0.0),
            food_patches=(
                FoodPatchConfig(
                    "food_a",
                    x=38,
                    y=14,
                    radius=3,
                    amount=120,
                    max_amount=120,
                    regrowth_rate=1,
                    relocate_on_depletion=False,
                ),
                FoodPatchConfig(
                    "food_b",
                    x=48,
                    y=35,
                    radius=4,
                    amount=180,
                    max_amount=180,
                    regrowth_rate=1,
                    relocate_on_depletion=False,
                ),
            ),
            disturbance_tick=150,
            disturbance_food_shift=True,
            disturbance_food_shift_dx=-8,
            disturbance_food_shift_dy=6,
            disturbance_kill_radius=4,
            ants=AntAgentConfig(
                max_age=240,
                max_population=44,
                spawn_food_cost=2,
                spawn_interval=6,
                pheromone_enabled=True,
                hunger_return_threshold=5.0,
                nest_feed_amount=4.0,
            ),
        )
    )
    event_types = {event.event_type for event in result.events}
    assert "disturbance" in event_types
    assert "food_shift" in event_types
    tick_summaries = [event.payload for event in result.events if event.event_type == "tick_summary"]
    pre = tick_summaries[110:150]
    post = tick_summaries[200:240]
    pre_unloads = sum(item["unloads"] for item in pre)
    post_unloads = sum(item["unloads"] for item in post)
    assert pre_unloads > 0
    assert post_unloads > 0
