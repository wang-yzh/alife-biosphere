from __future__ import annotations

from dataclasses import dataclass, field

from .config import WorldConfig
from .events import Event
from .habitat import Habitat
from .organism import Organism


@dataclass
class World:
    tick: int
    habitats: dict[str, Habitat]
    organisms: dict[str, Organism]
    next_organism_index: int = 0
    events: list[Event] = field(default_factory=list)

    @classmethod
    def from_config(cls, config: WorldConfig) -> "World":
        habitats = {item.habitat_id: Habitat.from_config(item) for item in config.habitats}
        adjacency: dict[str, set[str]] = {habitat_id: set() for habitat_id in habitats}
        for left, right in config.habitat_edges:
            adjacency[left].add(right)
            adjacency[right].add(left)
        for habitat_id, neighbors in adjacency.items():
            habitats[habitat_id].set_neighbors(tuple(sorted(neighbors)))
        habitat_ids = cls._founder_seed_order(habitats)
        organisms: dict[str, Organism] = {}
        for index in range(config.founder_count):
            habitat_id = habitat_ids[index % len(habitat_ids)]
            organism = Organism.founder(f"org_{index:03d}", habitat_id, config.organism)
            organisms[organism.organism_id] = organism
            habitats[habitat_id].occupants.add(organism.organism_id)
        return cls(
            tick=0,
            habitats=habitats,
            organisms=organisms,
            next_organism_index=config.founder_count,
        )

    @staticmethod
    def _founder_seed_order(habitats: dict[str, Habitat]) -> tuple[str, ...]:
        preferred = [
            habitat_id
            for habitat_id, habitat in habitats.items()
            if habitat.habitat_family in {"nursery", "refuge"}
        ]
        if preferred:
            return tuple(sorted(preferred))
        return tuple(sorted(habitats))

    def alive_count(self) -> int:
        return sum(1 for organism in self.organisms.values() if organism.alive)

    def reproduction_ready_count(self) -> int:
        return sum(1 for organism in self.organisms.values() if organism.alive and organism.reproduction_ready)

    def occupancy_by_habitat(self) -> dict[str, int]:
        return {habitat_id: len(habitat.occupants) for habitat_id, habitat in self.habitats.items()}

    def emit(self, event: Event) -> None:
        self.events.append(event)

    def allocate_organism_id(self) -> str:
        organism_id = f"org_{self.next_organism_index:03d}"
        self.next_organism_index += 1
        return organism_id

    def add_organism(self, organism: Organism) -> None:
        self.organisms[organism.organism_id] = organism
        self.habitats[organism.habitat_id].occupants.add(organism.organism_id)

    def move_organism(self, organism_id: str, destination_id: str) -> None:
        organism = self.organisms[organism_id]
        origin_id = organism.habitat_id
        if origin_id == destination_id:
            return
        self.habitats[origin_id].occupants.remove(organism_id)
        self.habitats[destination_id].occupants.add(organism_id)
        organism.last_habitat_id = origin_id
        organism.habitat_id = destination_id

    def remove_from_habitat(self, organism_id: str) -> None:
        organism = self.organisms[organism_id]
        habitat = self.habitats[organism.habitat_id]
        habitat.occupants.discard(organism_id)
