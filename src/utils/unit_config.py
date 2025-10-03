"""
Unit system configuration and conversion utilities.

Supports both US (lb-in-F) and Metric (N-mm-C) unit systems.
"""

from enum import Enum
from dataclasses import dataclass


class UnitSystem(Enum):
    """Enumeration of supported unit systems."""
    US = "US"  # lb-in-F
    METRIC = "Metric"  # N-mm-C


@dataclass
class UnitConfig:
    """Configuration for unit system."""
    system: UnitSystem
    etabs_unit_code: int
    length_unit: str  # "in" or "mm"
    force_unit: str   # "lb" or "N"
    temp_unit: str    # "F" or "C"
    story_input_unit: str  # "ft" or "m"

    # Conversion factors to ETABS internal units
    length_to_model: float  # Convert input to model units
    force_to_model: float   # Convert input to model units


# Predefined unit configurations
US_UNITS = UnitConfig(
    system=UnitSystem.US,
    etabs_unit_code=1,
    length_unit="in",
    force_unit="lb",
    temp_unit="F",
    story_input_unit="ft",
    length_to_model=12.0,  # ft to inches
    force_to_model=1.0     # lb to lb
)

METRIC_UNITS = UnitConfig(
    system=UnitSystem.METRIC,
    etabs_unit_code=9,
    length_unit="mm",
    force_unit="N",
    temp_unit="C",
    story_input_unit="m",
    length_to_model=1000.0,  # m to mm
    force_to_model=1.0       # N to N
)


def get_unit_config(system: UnitSystem) -> UnitConfig:
    """
    Get unit configuration for the specified system.

    Args:
        system: Unit system (US or METRIC)

    Returns:
        UnitConfig object
    """
    if system == UnitSystem.US:
        return US_UNITS
    elif system == UnitSystem.METRIC:
        return METRIC_UNITS
    else:
        raise ValueError(f"Unsupported unit system: {system}")


def convert_story_height(height: float, unit_config: UnitConfig) -> float:
    """
    Convert story height from input units to model units.

    Args:
        height: Height in input units (ft or m)
        unit_config: Unit configuration

    Returns:
        Height in model units (inches or mm)
    """
    return height * unit_config.length_to_model


def convert_load(load: float, unit_config: UnitConfig, from_area: bool = False) -> float:
    """
    Convert load from input units to model units.

    Args:
        load: Load value
        unit_config: Unit configuration
        from_area: True if converting area load (psf or kN/m²)

    Returns:
        Load in model units
    """
    if unit_config.system == UnitSystem.US:
        # US: psf to psi (divide by 144)
        if from_area:
            return load / 144.0
        return load
    else:
        # Metric: Already in correct units (N/mm²)
        return load


def print_unit_info(unit_config: UnitConfig):
    """Print unit system information."""
    print(f"\n📏 Unit System: {unit_config.system.value}")
    print(f"   Length: {unit_config.length_unit}")
    print(f"   Force: {unit_config.force_unit}")
    print(f"   Temperature: {unit_config.temp_unit}")
    print(f"   Story Input: {unit_config.story_input_unit}")