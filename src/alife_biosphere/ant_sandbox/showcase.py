from __future__ import annotations

from dataclasses import replace
from math import dist

from ..rng import make_rng
from .config import AntAgentConfig, AntSandboxConfig, ColonyConfig, FoodPatchConfig, NestConfig, TerrainConfig


def _randomized_food_patches(seed: int, colonies: tuple[ColonyConfig, ...]) -> tuple[FoodPatchConfig, ...]:
    rng = make_rng(seed, "ant-sandbox:showcase:food")
    specs = [
        ("food_northwest", 0.28, 0.24, 4, 34, 0.9, 16),
        ("food_north", 0.55, 0.18, 5, 56, 1.0, 18),
        ("food_mid", 0.52, 0.50, 5, 68, 1.1, 20),
        ("food_southeast", 0.78, 0.72, 7, 120, 1.45, 24),
        ("food_south", 0.60, 0.82, 6, 84, 1.2, 22),
        ("food_far_east", 0.86, 0.42, 6, 92, 1.35, 24),
    ]
    patches: list[FoodPatchConfig] = []
    for patch_id, px, py, radius, amount, value_score, respawn_delay in specs:
        jitter_x = rng.randint(-6, 6)
        jitter_y = rng.randint(-5, 5)
        amount_jitter = rng.randint(-10, 14)
        value_jitter = rng.uniform(-0.08, 0.12)
        x = max(10, min(118, int(round(128 * px)) + jitter_x))
        y = max(10, min(86, int(round(96 * py)) + jitter_y))
        min_nest_distance = radius + 16
        if any(dist((x, y), (colony.nest.x, colony.nest.y)) < min_nest_distance for colony in colonies):
            for _ in range(120):
                candidate_x = rng.randint(12, 116)
                candidate_y = rng.randint(12, 84)
                if all(
                    dist((candidate_x, candidate_y), (colony.nest.x, colony.nest.y)) >= min_nest_distance
                    for colony in colonies
                ):
                    x = candidate_x
                    y = candidate_y
                    break
        final_amount = max(20, amount + amount_jitter)
        patches.append(
            FoodPatchConfig(
                patch_id=patch_id,
                x=x,
                y=y,
                radius=radius,
                amount=final_amount,
                max_amount=final_amount,
                value_score=max(0.65, round(value_score + value_jitter, 2)),
                regrowth_rate=0,
                respawn_delay_ticks=respawn_delay,
            )
        )
    return tuple(patches)


def build_showcase_config(seed: int = 7, ticks: int = 1800) -> AntSandboxConfig:
    colonies = (
        ColonyConfig(
            colony_id="wei",
            display_name="Wei",
            color="#375a7f",
            ant_count=11,
            nest=NestConfig(x=18, y=48, radius=4, initial_stored_food=10, colony_upkeep_per_ant_tick=0.0035),
        ),
        ColonyConfig(
            colony_id="shu",
            display_name="Shu",
            color="#b24a3a",
            ant_count=11,
            nest=NestConfig(x=98, y=18, radius=4, initial_stored_food=10, colony_upkeep_per_ant_tick=0.0035),
        ),
        ColonyConfig(
            colony_id="wu",
            display_name="Wu",
            color="#2f8f5b",
            ant_count=10,
            nest=NestConfig(x=80, y=66, radius=4, initial_stored_food=10, colony_upkeep_per_ant_tick=0.0035),
        ),
    )
    ants = AntAgentConfig(
        ant_count=32,
        max_population=32,
        max_age=2600,
        allow_spawning=False,
        food_sense_radius=22,
        pheromone_sense_radius=12,
        metabolism_cost=0.05,
        hunger_return_threshold=6.5,
        trail_deposit=1.6,
        home_trail_deposit=0.85,
        trail_decay=0.028,
        hostility_radius=4,
        hostility_weight=1.15,
        foreign_trail_weight=0.3,
        combat_enabled=True,
        combat_radius=2,
        combat_duration=8,
        combat_cooldown=5,
        combat_decision_threshold=0.85,
    )
    return AntSandboxConfig(
        seed=seed,
        ticks=ticks,
        width=128,
        height=96,
        nest=colonies[0].nest,
        colonies=colonies,
        food_patches=_randomized_food_patches(seed, colonies),
        ants=ants,
        terrain=TerrainConfig(enabled=True, layout="surface_showcase_walls"),
    )
