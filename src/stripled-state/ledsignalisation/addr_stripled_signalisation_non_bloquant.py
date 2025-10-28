"""

    https://core-electronics.com.au/guides/raspberry-pi/fully-addressable-rgb-raspberry-pi/


    sudo pip3 install rpi_ws281x
    sudo pip3 install adafruit-circuitpython-neopixel
    sudo python3 -m pip install --force-reinstall adafruit-blinka

    Controle de 3 groupe de 2 stripled sans delay avec 3 GPIO de la Raspberry Pi
    Chaque méthode détermine un état du robot (hello, booting, ready,  danger, turn...)



    include all neccessary packages to get LEDs to work with Raspberry Pi

"""
import time
import board
import neopixel



class AddrStripLedSignalisationNonBloquant:
    def __init__(self):
        self.nbre_stripled = 10

        self.ready_last_time = 0
        self.danger_last_time = 0

        self.booting_last_time = 0
        """False = led eteinte True = led allumée"""
        self.booting_stripled_is_on = False

        self.turn_last_time = 0
        self.turn_step = 0 #les differentes séquences
        self.turn_index = 0
        self.turn_start = 0
        
        self.hello_last_time = 0
        self.hello_step = 0 #les differentes séquences

        self.hello_index = 0
        self.hello_color_index = 0


        """
        couleur : null, rouge, vert, bleu, jaune
        """
        self.off = (0, 0, 0)
        self.color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        """
        NeoPixel(GPIO, Nbreled, luminositer)
        """
        self.left_stripled = neopixel.NeoPixel(board.D12, self.nbre_stripled, brightness=1)
        self.right_stripled = neopixel.NeoPixel(board.D13, self.nbre_stripled, brightness=1)
        self.middle_stripled = neopixel.NeoPixel(board.D21, self.nbre_stripled, brightness=1) 


    def turn_off_all_stripled(self):
        self.left_stripled.fill(self.off)
        self.right_stripled.fill(self.off)
        self.middle_stripled.fill(self.off)

    """Toutes les LEDs en vert"""
    def ready(self):
        #print("ready...")
        current_time = time.time()
        if current_time - self.ready_last_time >= 0.2:
            self.left_stripled.fill(self.color[1])
            self.right_stripled.fill(self.color[1])
            self.middle_stripled.fill(self.color[1])

            self.ready_last_time = current_time

    """Toutes les LEDs en rouge"""
    def danger(self):
        #print("danger...")
        current_time = time.time()
        if current_time - self.danger_last_time >= 0.2:
            self.left_stripled.fill(self.color[0])
            self.right_stripled.fill(self.color[0])
            self.middle_stripled.fill(self.color[0])

            self.danger_last_time = current_time

    """Clignotement simple de toutes les LEDs en vert"""
    def booting(self):
        #print("booting...")
        current_time = time.time()
        if current_time - self.booting_last_time >= 0.2:
            if self.booting_stripled_is_on == False:
                self.left_stripled.fill(self.color[1])
                self.right_stripled.fill(self.color[1])
                self.middle_stripled.fill(self.color[1])
                self.booting_stripled_is_on = True
            else:
                self.turn_off_all_stripled()
                self.booting_stripled_is_on = False

            self.booting_last_time = current_time


   

    """
    recupere le coté où l'on veut tourner et renvoit la bande de led à actionner 
    """
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
        current_time = time.time()

        if current_time - self.turn_last_time >= 0.2:

            if self.turn_step in [0, 2]:

                active_stripled.fill(self.color[3])
                self.turn_step += 1
                
            elif self.turn_step in [1, 3]:
                # ÉTAPE 1 ou 3 : OFF (Éteindre)
                active_stripled.fill(self.off)
                self.turn_step += 1


            elif self.turn_step == 4:
                if self.turn_index < self.nbre_stripled:
                    active_stripled[self.turn_index] = self.color[3]
                    active_stripled.show()
                    self.turn_index += 1
                else:
                    self.turn_off_all_stripled()
                    self.turn_index = 0
                    self.turn_step += 1


            elif self.turn_step == 5:
                
                if self.turn_start  <= (self.nbre_stripled - 3):
                    active_stripled.fill(self.off) 
                    # 2. Allumer la fenêtre de 3 LEDs
                    for i in range(3):

                        active_stripled[self.turn_start + i] = self.color[3]  # allumer les LEDs de la fenêtre
                        active_stripled.show()

                    self.turn_start += 1
                else:
                    #print("Turn sequence complete ...")
                    self.turn_off_all_stripled()
                    self.turn_index = 0
                    self.turn_start = 0
                    self.turn_step = 0
                    
            # Mettre à jour le chronomètre UNIQUEMENT après l'action
            self.turn_last_time = current_time

    """
    Salutation
    Allumage de toutes les leds en vert puis en jaune puis en rouge
    Chaque led de chaque segment s'allument avec une couleure différente du début à la fin de facon progressive
    """
        
    def hello(self):
        #print("hello...")
        
        current_time = time.time()
        if self.hello_step < 6 and current_time - self.hello_last_time >= 0.5:
            if self.hello_step == 0:
                #etat 0 les led s'allument en vert
                self.left_stripled.fill(self.color[1])
                self.right_stripled.fill(self.color[1])
                self.middle_stripled.fill(self.color[1])
                self.hello_step = 1

            elif self.hello_step == 1:
                #etat 1 les led s'éteignent
                self.turn_off_all_stripled()
                self.hello_step = 2

            elif self.hello_step == 2:
                
                self.left_stripled.fill(self.color[3])
                self.right_stripled.fill(self.color[3])
                self.middle_stripled.fill(self.color[3])
                self.hello_step = 3

            elif self.hello_step == 3:
                
                self.turn_off_all_stripled()
                self.hello_step = 4
            
            elif self.hello_step == 4:
                self.left_stripled.fill(self.color[0])
                self.right_stripled.fill(self.color[0])
                self.middle_stripled.fill(self.color[0])
                self.hello_step = 5

            elif self.hello_step == 5:
                
                self.turn_off_all_stripled()
                self.hello_step = 6

            self.hello_last_time = current_time
                
        
        
        if self.hello_step == 6:
            if current_time - self.hello_last_time >= 0.2:
                if self.hello_index < self.nbre_stripled:
    
                    self.left_stripled[self.hello_index] = self.color[self.hello_color_index]
                    self.left_stripled.show()
                    self.right_stripled[self.hello_index] = self.color[self.hello_color_index]
                    self.right_stripled.show()
                    self.middle_stripled[self.hello_index] = self.color[self.hello_color_index]
                    self.middle_stripled.show()
                    
                    self.hello_color_index = (self.hello_color_index + 1) % len(self.color)
                    self.hello_index += 1

                else:

                    #print("hello termné ...")
                    self.hello_index = 0
                    self.hello_color_index = 0
                    self.hello_step = 0 
                    self.turn_off_all_stripled()
                

                self.hello_last_time = current_time
                            

