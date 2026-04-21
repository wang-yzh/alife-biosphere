"""Core package for the artificial-life biosphere scaffold."""

from .config import HabitatConfig, OrganismConfig, SimulationConfig, WorldConfig
from .observer import build_observer_payload
from .observer import write_observer_html
from .reporting import summarize_disturbance_recovery
from .reporting import summarize_source_sink_roles
from .simulation import run_simulation

__all__ = [
    "HabitatConfig",
    "OrganismConfig",
    "SimulationConfig",
    "WorldConfig",
    "build_observer_payload",
    "summarize_disturbance_recovery",
    "summarize_source_sink_roles",
    "run_simulation",
    "write_observer_html",
]
