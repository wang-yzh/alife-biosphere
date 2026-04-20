from __future__ import annotations

from dataclasses import dataclass

from .config import OrganismConfig


@dataclass
class Organism:
    organism_id: str
    lineage_id: str
    parent_id: str | None
    habitat_id: str
    energy: float
    matter: float
    integrity: float
    information: float
    age: int = 0
    generation: int = 0
    birth_tick: int = 0
    life_stage: str = "juvenile"
    reproduction_ready: bool = False
    death_reason: str | None = None
    last_habitat_id: str | None = None
    movement_cooldown: int = 0
    alive: bool = True

    @classmethod
    def founder(cls, organism_id: str, habitat_id: str, config: OrganismConfig) -> "Organism":
        return cls(
            organism_id=organism_id,
            lineage_id=organism_id,
            parent_id=None,
            habitat_id=habitat_id,
            energy=config.initial_energy,
            matter=config.initial_matter,
            integrity=config.initial_integrity,
            information=config.initial_information,
        )

    def begin_tick(self, metabolism_cost: float, maturity_age: int, senescence_age: int) -> None:
        if not self.alive:
            return
        self.age += 1
        self.movement_cooldown = max(0, self.movement_cooldown - 1)
        self.energy = max(0.0, self.energy - metabolism_cost)
        if self.energy == 0.0:
            self.integrity = max(0.0, self.integrity - 0.2)
        self.update_life_stage(maturity_age, senescence_age)
        if self.life_stage == "senescent":
            self.integrity = max(0.0, self.integrity - 0.03)
        if self.integrity <= 0.0:
            self.die("integrity_depleted")

    def harvest(self, amount: float, repair_gain_scale: float) -> float:
        if not self.alive:
            return 0.0
        self.energy += amount
        self.matter += amount * 0.25
        self.information += 0.1
        repair = min(1.0 - self.integrity, amount * repair_gain_scale)
        self.integrity = min(1.0, self.integrity + repair)
        return repair

    def update_life_stage(self, maturity_age: int, senescence_age: int) -> None:
        if not self.alive:
            self.life_stage = "dead"
        elif self.age >= senescence_age:
            self.life_stage = "senescent"
        elif self.age >= maturity_age:
            self.life_stage = "mature"
        else:
            self.life_stage = "juvenile"

    def apply_damage(self, amount: float, reason: str) -> float:
        if not self.alive or amount <= 0.0:
            return 0.0
        applied = min(self.integrity, amount)
        self.integrity = max(0.0, self.integrity - applied)
        if self.integrity <= 0.0:
            self.die(reason)
        return applied

    def die(self, reason: str) -> bool:
        if not self.alive:
            return False
        self.alive = False
        self.integrity = 0.0
        self.reproduction_ready = False
        self.death_reason = reason
        self.life_stage = "dead"
        return True
