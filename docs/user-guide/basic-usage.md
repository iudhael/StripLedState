# Basic Usage

This guide covers the fundamental concepts and operations in MeMaMate Signal

## Core Concepts

###  AddrStripLedSignalisationNonBloquant, Speaker, Microphone

MeMaMate Signal uses a Three-layer architecture:

- **AddrStripLedSignalisationNonBloquant**: for strip led control
- **Speaker**: For sound
- **Microphone**: For microphone

```python
from mecamatesignal import AddrStripLedSignalisationNonBloquant2
from mecamatesignal import EmergencySignal
from mecamatesignal import Speaker
from mecamatesignal import Microphone


def main():
    #speaker = Speaker()
    #mic = Microphone()
    leds = AddrStripLedSignalisationNonBloquant2()
    emergency_signal = EmergencySignal()
    
    while(1):
        #signal 'arret d'urgence
        emergency_signal.emergencySignal()

        leds.ready()

    
    
if __name__ == "__main__":
    main()
```



## Next Steps

Now that you understand basic usage:

- [CLI Guide](cli.md) - Command-line interface for testing
- [API Reference](../api-reference/) - Complete method documentation
