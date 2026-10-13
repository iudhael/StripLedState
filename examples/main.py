from StripLedState import AddrStripLedSignalisationNonBloquantV2


def main():

    leds = AddrStripLedSignalisationNonBloquantV2(10)

    
    while(1):

        
        #leds.pre_operational(1)
        #leds.ready(1)
        #leds.emergency_stop(1)
        #leds.ready_to_go(1)
        #leds.turning("droite", 1)
        #leds.braking(1)
        #leds.reverse(1)
        leds.hello(1)

        #leds.turn_off_all_stripled()


    
    
    
if __name__ == "__main__":
    main()



