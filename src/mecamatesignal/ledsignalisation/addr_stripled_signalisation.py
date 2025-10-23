"""

    #https://core-electronics.com.au/guides/raspberry-pi/fully-addressable-rgb-raspberry-pi/


    #sudo pip3 install rpi_ws281x
    #sudo pip3 install adafruit-circuitpython-neopixel
    #sudo python3 -m pip install --force-reinstall adafruit-blinka

    #Controle de 3 groupe de 2 stripled avec delay et3 GPIO de la raspberry Pi
    # Chaque méthode détermine un état du robot (hello, booting, danger, turn...)


    #include all neccessary packages to get LEDs to work with Raspberry Pi
"""
import time
import board
import neopixel



class AddrStripLedSignalisation:
    def __init__(self):
    
        """
        couleur : null, rouge, vert, bleu, jaune
        """
        self.off = (0, 0, 0)
        self.color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        #NeoPixel(GPIO, Nbreled, luminositer)
        self.left_stripled = neopixel.NeoPixel(board.D12, 10, brightness=1)
        self.right_stripled = neopixel.NeoPixel(board.D13, 10, brightness=1)
        self.middle_stripled = neopixel.NeoPixel(board.D21, 10, brightness=1) 

    def turn_off__all_stripled(self):
        self.left_stripled.fill(self.off)
        self.right_stripled.fill(self.off)
        self.middle_stripled.fill(self.off)

    """Toutes les LEDs en vert"""
    def ready(self):
        #print("ready...")
        self.left_stripled.fill(self.color[1])
        self.right_stripled.fill(self.color[1])
        self.middle_stripled.fill(self.color[1])
        time.sleep(0.2)

    """Toutes les LEDs en rouge"""
    def danger(self):
        #print("danger...")
        self.left_stripled.fill(self.color[0])
        self.right_stripled.fill(self.color[0])
        self.middle_stripled.fill(self.color[0])
        time.sleep(0.2)
   
    """Clignotement simple de toutes les LEDs en vert"""
    def booting(self):
        #print("booting...")
        self.left_stripled.fill(self.color[1])
        self.right_stripled.fill(self.color[1])
        self.middle_stripled.fill(self.color[1])

        time.sleep(0.2)

        self.turn_off__all_stripled()
        
        time.sleep(0.2)
        
    """
    Salutation
    Allumage de toutes les leds en vert puis en jaune puis en rouge
    Chaque led de chaque segment s'allument avec une couleure différente du début à la fin de facon progressive
    """
    def hello(self):
        #print("hello...")
        
        
        self.left_stripled.fill(self.color[1])
        self.right_stripled.fill(self.color[1])
        self.middle_stripled.fill(self.color[1])

        time.sleep(0.5)
        
        self.turn_off__all_stripled()
        
        time.sleep(0.5)
        
        self.left_stripled.fill(self.color[3])
        self.right_stripled.fill(self.color[3])
        self.middle_stripled.fill(self.color[3])

        time.sleep(0.5)
        
        self.turn_off__all_stripled()
        
        time.sleep(0.5)
        
        self.left_stripled.fill(self.color[0])
        self.right_stripled.fill(self.color[0])
        self.middle_stripled.fill(self.color[0])

        time.sleep(0.5)
        
        self.turn_off__all_stripled()
        
        time.sleep(0.5)
        
        
        
        j=0
        for i in range(len(self.right_stripled)):
            
            if j < len(self.color):
                self.left_stripled[i] = self.color[j]
                self.left_stripled.show()
                self.right_stripled[i] = self.color[j]
                self.right_stripled.show()
                self.middle_stripled[i] = self.color[j]
                self.middle_stripled.show()
                j += 1
                
            else:
                j=0
            time.sleep(0.2)
            


        
 
        self.turn_off__all_stripled()
        time.sleep(0.2)

    #recupere le coté où l'on veut tourner et renvoit la bande de led à actionner 
    def get_turn_stripled(self, direction):
        if direction == "gauche":
            self.right_stripled.fill(self.off)
            self.middle_stripled.fill(self.off)
            
            return self.left_stripled

        if direction == "droite":
            self.left_stripled.fill(self.off)
            self.middle_stripled.fill(self.off)
            
            return self.right_stripled
        return None


    """
    Indique si le robot veut tourner à gauche ou à droite
    Séquence de clignotement x2
    Allumage successif des leds de chaque segement de la direction
    Effet de mouvement de 3 leds qui se déplacent étant allumé
    """
    def turn(self, direction):
        active_stripled = self.get_turn_stripled(direction)
        #(255, 255, 0) : jaune
        #print(f"turn... {direction}")

        active_stripled.fill(self.color[3])

        time.sleep(0.2)
        
        active_stripled.fill(self.off)

        time.sleep(0.2)

        active_stripled.fill(self.color[3])
        
        time.sleep(0.2)
                
        active_stripled.fill(self.off)

        time.sleep(0.5)

        for i in range(len(active_stripled)):
            active_stripled[i] = self.color[3]
            active_stripled.show()
            time.sleep(0.2)

        active_stripled.fill(self.off)
        active_stripled.show()

        time.sleep(0.5)
        
        for start in range(len(active_stripled) - 3): #len(active_stripled) - 3 + 1)
            active_stripled.fill(self.off)  # éteindre toutes les LEDs
            for i in range(3):
                active_stripled[start + i] = self.color[3]  # allumer les LEDs de la fenêtre
            active_stripled.show()
            time.sleep(0.3)
            active_stripled.fill(self.off)
            








