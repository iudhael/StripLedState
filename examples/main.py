from mecamatesignal import AddrStripLedSignalisationNonBloquant2
from mecamatesignal import EmergencySignal
from mecamatesignal import Speaker
from mecamatesignal import Microphone
import time

def main():
    speaker = Speaker()
    mic = Microphone()
    leds = AddrStripLedSignalisationNonBloquant2()
    emergency_signal = EmergencySignal()
    
    while(1):
        #signal 'arret d'urgence
        emergency_signal.emergencySignal()

        leds.ready()
        time.sleep(3)
        leds.danger()
        time.sleep(3)
        leds.booting()
        time.sleep(3)
        leds.hello()
        time.sleep(3)
        leds.turn(direction="droite")
        time.sleep(3)
    
    
    
if __name__ == "__main__":
    main()



