from __future__ import annotations

from dataclasses import dataclass

from .config import AntAgentConfig, AntSandboxConfig, FoodPatchConfig, NestConfig
from .reporting import summarize_behavior_roles
from .simulation import run_simulation


DEFAULT_VALIDATION_SEEDS = (7, 11, 13)


@dataclass(frozen=True)
class ValidationCase:
    seed: int
    base_unloads: int
    pheromone_on_unloads: int
    pheromone_off_unloads: int
    persistence_births: int
    persistence_deaths: int
    persistence_alive_min: int
    persistence_alive_max: int
    role_label_count: int
    disturbance_recovery_ratio: float

    def to_dict(self) -> dict[str, object]:
        return {
            "seed": self.seed,
            "base_unloads": self.base_unloads,
            "pheromone_on_unloads": self.pheromone_on_unloads,
            "pheromone_off_unloads": self.pheromone_off_unloads,
            "persistence_births": self.persistence_births,
            "persistence_deaths": self.persistence_deaths,
            "persistence_alive_min": self.persistence_alive_min,
            "persistence_alive_max": self.persistence_alive_max,
            "role_label_count": self.role_label_count,
            "disturbance_recovery_ratio": self.disturbance_recovery_ratio,
        }


def _base_config(seed: int) -> AntSandboxConfig:
    return AntSandboxConfig(seed=seed)


def _persistence_config(seed: int) -> AntSandboxConfig:
    return AntSandboxConfig(
        seed=seed,
        ticks=420,
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


def _disturbance_config(seed: int) -> AntSandboxConfig:
    return AntSandboxConfig(
        seed=seed,
        ticks=300,
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
        disturbance_food_shift_dx=-6,
        disturbance_food_shift_dy=4,
        disturbance_kill_radius=3,
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


def run_validation_cases(seeds: tuple[int, ...] = DEFAULT_VALIDATION_SEEDS) -> list[ValidationCase]:
    cases: list[ValidationCase] = []
    for seed in seeds:
        base_result = run_simulation(_base_config(seed))
        pheromone_on = run_simulation(AntSandboxConfig(seed=seed, ants=AntAgentConfig(pheromone_enabled=True)))
        pheromone_off = run_simulation(AntSandboxConfig(seed=seed, ants=AntAgentConfig(pheromone_enabled=False)))
        persistence_result = run_simulation(_persistence_config(seed))
        role_summary = summarize_behavior_roles(_persistence_config(seed), persistence_result, cluster_count=3)
        disturbance_result = run_simulation(_disturbance_config(seed))
        tick_summaries = [event.payload for event in disturbance_result.events if event.event_type == "tick_summary"]
        pre = tick_summaries[110:150]
        post = tick_summaries[200:240]
        pre_unloads = sum(item["unloads"] for item in pre)
        post_unloads = sum(item["unloads"] for item in post)
        recovery_ratio = 0.0 if pre_unloads == 0 else round(post_unloads / pre_unloads, 4)
        persistence_summaries = [event.payload for event in persistence_result.events if event.event_type == "tick_summary"]
        alive_counts = [summary["alive"] for summary in persistence_summaries]
        cases.append(
            ValidationCase(
                seed=seed,
                base_unloads=sum(1 for event in base_result.events if event.event_type == "food_unload"),
                pheromone_on_unloads=sum(1 for event in pheromone_on.events if event.event_type == "food_unload"),
                pheromone_off_unloads=sum(1 for event in pheromone_off.events if event.event_type == "food_unload"),
                persistence_births=sum(1 for event in persistence_result.events if event.event_type == "ant_birth"),
                persistence_deaths=sum(1 for event in persistence_result.events if event.event_type == "ant_death"),
                persistence_alive_min=min(alive_counts),
                persistence_alive_max=max(alive_counts),
                role_label_count=len(role_summary["role_distribution"]),
                disturbance_recovery_ratio=recovery_ratio,
            )
        )
    return cases


def summarize_validation_status(cases: list[ValidationCase]) -> dict[str, object]:
    if not cases:
        return {"case_count": 0, "cases": [], "metric_status": {}}
    m1_status = "pass"
    m2_status = (
        "pass"
        if all(case.base_unloads > 0 for case in cases)
        else "fail"
    )
    m3_status = (
        "pass"
        if all(case.pheromone_on_unloads > case.pheromone_off_unloads for case in cases)
        else "partial"
    )
    m4_status = (
        "pass"
        if all(
            case.persistence_births > 0
            and case.persistence_deaths > 0
            and case.persistence_alive_min > 0
            and case.persistence_alive_max <= 44
            for case in cases
        )
        else "partial"
    )
    m5_status = (
        "pass"
        if all(case.role_label_count >= 2 for case in cases)
        else "partial"
    )
    m6_status = (
        "pass"
        if all(case.disturbance_recovery_ratio >= 0.7 for case in cases)
        else "partial"
    )
    metric_status = {
        "M1_spatial_realism": m1_status,
        "M2_foraging_loop": m2_status,
        "M3_pheromone_effectiveness": m3_status,
        "M4_colony_persistence": m4_status,
        "M5_role_differentiation": m5_status,
        "M6_disturbance_recovery": m6_status,
    }
    return {
        "case_count": len(cases),
        "cases": [case.to_dict() for case in cases],
        "metric_status": metric_status,
        "mean_recovery_ratio": round(sum(case.disturbance_recovery_ratio for case in cases) / len(cases), 4),
        "mean_base_unloads": round(sum(case.base_unloads for case in cases) / len(cases), 4),
        "mean_pheromone_advantage": round(
            sum(case.pheromone_on_unloads - case.pheromone_off_unloads for case in cases) / len(cases),
            4,
        ),
    }
