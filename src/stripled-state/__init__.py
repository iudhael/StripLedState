"""StripLed State - Python library for MecaMate stripled signalisation.
"""

from . import addr_stripled_signalisation_non_bloquant_V2
# Version info
__version__ = "0.1.0"
__author__ = "MecaMate StripLed State"
__description__ = "MecaMate stripled signalisation"

# Public API exports
__all__ = [
    "turn_off_all_stripled",
    "pre_operational",
    "ready",
    "emergency_stop",
    "ready_to_go",
    "turning",
    "braking",
    "reverse",
    "hello"

]
