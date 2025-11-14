"""StripLed State - Python library for MecaMate stripled signalisation."""

# Import *symbols* from the V2 module so they exist at the top level
from .addr_stripled_signalisation_non_bloquant_V2 import (
    # class (adjust the name below if your class is slightly different)
    AddrStripLedSignalisationNonBloquantV2,
    # # module-level helper functions you listed in __all__
    # turn_off_all_stripled,
    # pre_operational,
    # ready,
    # emergency_stop,
    # ready_to_go,
    # turning,
    # turning_braking,
    # braking,
    # reverse,
    # hello,
)

__version__ = "0.1.0"
__author__ = "MecaMate StripLed State"
__description__ = "MecaMate stripled signalisation"

__all__ = [
    # classes
    "AddrStripLedSignalisationNonBloquantV2",
    # # functions
    # "turn_off_all_stripled",
    # "pre_operational",
    # "ready",
    # "emergency_stop",
    # "ready_to_go",
    # "turning",
    # turning_braking,
    # "braking",
    # "reverse",
    # "hello",
]
