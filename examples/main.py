from StripLedState import AddrStripLedSignalisationNonBloquant2


def main():

    leds = AddrStripLedSignalisationNonBloquant2(9)

    
    while(1):

        
        #leds.pre_operational()
        #leds.ready()
        #leds.emergency_stop()
        #leds.ready_to_go()
        #leds.turning("droite")
        #leds.braking()
        #leds.reverse()
        leds.hello()

        #leds.turn_off_all_stripled()


    
    
    
if __name__ == "__main__":
    main()



