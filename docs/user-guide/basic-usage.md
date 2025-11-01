# Basic Usage

This guide covers the fundamental concepts and operations in MeMaMate Signal

## Core Concepts

###  AddrStripLedSignalisationNonBloquant, Speaker, Microphone

MeMaMate Signal uses a Three-layer architecture:

- **AddrStripLedSignalisationNonBloquant**: for strip led control
- **Speaker**: For sound
- **Microphone**: For microphone

```python
from StripLedState import AddrStripLedSignalisationNonBloquant2


def main():

    leds = AddrStripLedSignalisationNonBloquant2(9)

    
    while(1):

        leds.ready()

    
    
if __name__ == "__main__":
    main()
```



## Next Steps

Now that you understand basic usage:

- [CLI Guide](cli.md) - Command-line interface for testing
- [API Reference](../api-reference/) - Complete method documentation
