# MecaMate Signal

**MecaMate Signal** Python library for robot signaling LED, sound (audio, microphone), emergency stop

## Installation

```bash
pip install mecamatesignal
```

For Raspberry Pi GPIO support:
```bash
pip install "mecamatesignal[pi]"
```

## Quick Start

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

