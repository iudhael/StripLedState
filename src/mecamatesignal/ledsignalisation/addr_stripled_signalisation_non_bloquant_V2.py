"""

    https://core-electronics.com.au/guides/raspberry-pi/fully-addressable-rgb-raspberry-pi/


    sudo pip3 install rpi_ws281x
    sudo pip3 install adafruit-circuitpython-neopixel
    sudo python3 -m pip install --force-reinstall adafruit-blinka

    Controle de 6 segments de  stripled sans delay avec un seul GPIO de la raspberry Pi
    Chaque méthode détermine un état du robot (hello, booting, danger, ready, turn...)



    #include all neccessary packages to get LEDs to work with Raspberry Pi

"""

import time
import board
import neopixel


NEOPIXEL_PIN = board.D12

class AddrStripLedSignalisationNonBloquant2:
    def __init__(self):
        """
            Chaque segment (gauche, droite, milieu) à 10 leds
        """
        self.nbre_led_par_segment = 10 
        self.nbre_led_total = 6 * self.nbre_led_par_segment  # 60 LEDs

        """
            Indices de début et de fin pour chaque segment dans la bande unique
        """
        """0 à 10"""
        self.start_front_left = 0 
        self.end_front_left = self.nbre_led_par_segment 
        
        """10 à 20"""
        self.start_back_left = self.nbre_led_par_segment
        self.end_back_left = 2 * self.nbre_led_par_segment

        """20 à 30"""
        self.start_back_middle = 2 * self.nbre_led_par_segment
        self.end_back_middle = 3 * self.nbre_led_par_segment

        """30 à 40"""
        self.start_back_right = 3 * self.nbre_led_par_segment
        self.end_back_right = 4 * self.nbre_led_par_segment
        
        """40 à 50"""
        self.start_front_right = 4 * self.nbre_led_par_segment
        self.end_front_right = 5 * self.nbre_led_par_segment

        """50 à 60"""
        self.start_front_middle = 5 * self.nbre_led_par_segment
        self.end_front_middle = self.nbre_led_total



        """ Variables de suivi d'état """
        self.ready_last_time = 0
        self.danger_last_time = 0

        self.booting_last_time = 0
        self.booting_stripled_is_on = False 

        self.turn_last_time = 0
        self.turn_step = 0 
        self.turn_index = 0
        self.turn_start = 0 
        
        self.hello_last_time = 0
        self.hello_step = 0 
        self.hello_index = 0
        self.hello_color_index = 0

        """ Couleurs off """
        self.off = (0, 0, 0)
        """ rouge, vert, bleu, jaune """
        self.color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

        """ 
        Création d'une seule instance NeoPixel pour toutes les LEDs sur une seule broche
        neopixel.NeoPixel(PIN, NbreledTotal, luminositer) 
        """
        
        self.all_stripled = neopixel.NeoPixel(
            NEOPIXEL_PIN, self.nbre_led_total, brightness=1, auto_write=False
        )
        self.all_stripled.fill(self.off)
        self.all_stripled.show()



    """Eteindre toutes les LEDs"""
    def turn_off_all_stripled(self):
        self.all_stripled.fill(self.off)
        self.all_stripled.show()

    """Remplit un segment spécifique de la bande avec une couleur"""
    def fill_segment(self, start, end, color):
        for i in range(start, end):
            self.all_stripled[i] = color
        self.all_stripled.show()
        
    """Renvoie les indices de début et de fin pour un segment donné."""
    def get_segment_indices(self, group_name):
        if group_name == "gauche":
            return self.start_front_left, self.end_front_left, self.start_back_left, self.end_back_left
        if group_name == "droite":
            return self.start_front_right, self.end_front_right, self.start_back_right, self.end_back_right
        if group_name == "milieu":
            return self.start_front_middle, self.end_front_middle, self.start_back_middle, self.end_back_middle
        return -1, -1


    """Etats"""

    """Toutes les LEDs en vert"""
    def ready(self):
        """print("ready...")"""
        current_time = time.time()
        if current_time - self.ready_last_time >= 0.2:
            self.all_stripled.fill(self.color[1]) # Vert
            self.all_stripled.show()
            self.ready_last_time = current_time
    
    """Toutes les LEDs en rouge"""
    def danger(self):
        """print("danger...")"""
        current_time = time.time()
        if current_time - self.danger_last_time >= 0.2:
            self.all_stripled.fill(self.color[0]) # Rouge
            self.all_stripled.show()
            self.danger_last_time = current_time
    
    """Clignotement simple de toutes les LEDs en vert"""
    def booting(self):
        """print("booting...")"""
        current_time = time.time()
        if current_time - self.booting_last_time >= 0.2:
            if self.booting_stripled_is_on == False:
                self.all_stripled.fill(self.color[1]) # Vert
                self.booting_stripled_is_on = True
            else:
                self.all_stripled.fill(self.off) # Éteint
                self.booting_stripled_is_on = False
            
            self.all_stripled.show()
            self.booting_last_time = current_time

    """
    Indique si le robot veut tourner à gauche ou à droite
    Séquence de clignotement x2
    Allumage successif des leds de chaque segement de la direction
    Effet de mouvement de 3 leds qui se déplacent étant allumé
    """
    def turn(self, direction):
        """print(f"turn... {direction}")"""
        current_time = time.time()

        start_front, end_front, start_back, end_back = self.get_segment_indices(direction)
        segment_length = self.nbre_led_par_segment

        if start_front == -1 or start_back == -1:
            return """Sortie si direction non valide"""

        """ Éteindre les autres segments pour isoler l'effet """
        if direction == "gauche":
            self.fill_segment(self.start_front_right, self.end_front_right, self.off)
            self.fill_segment(self.start_back_right, self.end_back_right, self.off)
            
            self.fill_segment(self.start_front_middle, self.end_front_middle, self.off)
            self.fill_segment(self.start_back_middle, self.end_back_middle, self.off)
        elif direction == "droite":
            self.fill_segment(self.start_front_left, self.end_front_left, self.off)
            self.fill_segment(self.start_back_left, self.end_back_left, self.off)
            
            self.fill_segment(self.start_front_middle, self.end_front_middle, self.off)
            self.fill_segment(self.start_back_middle, self.end_back_middle, self.off)


        if current_time - self.turn_last_time >= 0.2:
            color = self.color[3] # Jaune

            if self.turn_step in [0, 2]:
                """ ÉTAPE 0 ou 2 : ON (Allumer le segment complet)"""
                self.fill_segment(start_front, end_front, color)
                self.fill_segment(start_back, end_back, color)
                self.turn_step += 1 
            elif self.turn_step in [1, 3]:
                """ ÉTAPE 1 ou 3 : OFF (Éteindre le segment complet) """
                self.fill_segment(start_front, end_front, self.off)
                self.fill_segment(start_back, end_back, self.off)
                self.turn_step += 1

            elif self.turn_step == 4:
                """ ÉTAPE 4 : Allumage progressif LED par LED """
                if self.turn_index < segment_length:
                    self.all_stripled[start_front + self.turn_index] = color
                    self.all_stripled[start_back + self.turn_index] = color
                    self.all_stripled.show()
                    self.turn_index += 1
                else:
                    self.fill_segment(start_front, end_front, self.off) # Éteindre à la fin
                    self.fill_segment(start_back, end_back, self.off) # Éteindre à la fin
                    self.turn_index = 0
                    self.turn_step += 1

            elif self.turn_step == 5:
                """ ÉTAPE 5 : Fenêtre de 3 LEDs qui défilent """
                window_size = 3
                if self.turn_start <= (segment_length - window_size):
                    self.fill_segment(start_front, end_front, self.off) # Éteindre avant de défiler
                    self.fill_segment(start_back, end_back, self.off) # Éteindre avant de défiler

                    """ Allumer la fenêtre de 3 LEDs """
                    for i in range(window_size):
                        self.all_stripled[start_front + self.turn_start + i] = color 
                        self.all_stripled[start_back + self.turn_start + i] = color 
                        
                    self.all_stripled.show()


                    self.turn_start += 1
                else:
                    """ Séquence terminée """
                    """print("Turn sequence complete ...")"""
                    self.turn_off_all_stripled()
                    self.turn_index = 0
                    self.turn_start = 0
                    self.turn_step = 0
                    
            self.turn_last_time = current_time

    """
    Salutation
    Allumage de toutes les leds en vert puis en jaune puis en rouge
    Chaque led de chaque segment s'allument avec une couleure différente du début à la fin de facon progressive
    """
    def hello(self):
        """print("hello...")"""
        current_time = time.time()
        
        """ Séquence de clignotements couleur par couleur (Vert, Jaune, Rouge) """
        if self.hello_step < 6 and current_time - self.hello_last_time >= 0.5:
            """ Les steps 0, 2, 4 allument le bandeau total dans une couleur """
            if self.hello_step == 0: color_index = 1 # Vert
            elif self.hello_step == 2: color_index = 3 # Jaune
            elif self.hello_step == 4: color_index = 0 # Rouge
            else: color_index = -1 # Non utilisé

            if self.hello_step in [0, 2, 4]:
                self.all_stripled.fill(self.color[color_index])
            else: # steps 1, 3, 5 éteignent
                self.all_stripled.fill(self.off)
            
            self.all_stripled.show()
            self.hello_step += 1
            self.hello_last_time = current_time
                
        
        """ Séquence d'allumage progressif en arc-en-ciel (rainbow-like) """
        if self.hello_step == 6:
            if current_time - self.hello_last_time >= 0.2:
                if self.hello_index < self.nbre_led_par_segment:
                    color_to_use = self.color[self.hello_color_index]
    
                    """ Allumer la LED à l'index actuel dans la couleur """
                    self.all_stripled[self.start_front_left + self.hello_index] = color_to_use
                    self.all_stripled[self.start_back_left + self.hello_index] = color_to_use
                    
                    self.all_stripled[self.start_front_right + self.hello_index] = color_to_use
                    self.all_stripled[self.start_back_right + self.hello_index] = color_to_use
                    
                    self.all_stripled[self.start_front_middle + self.hello_index] = color_to_use
                    self.all_stripled[self.start_back_middle + self.hello_index] = color_to_use

                    self.all_stripled.show()
                    
                    self.hello_color_index = (self.hello_color_index + 1) % len(self.color)
                    self.hello_index += 1

                else:
                    """ Séquence terminée """
                    """ print("hello terminé ...") """
                    self.hello_index = 0
                    self.hello_color_index = 0
                    self.hello_step = 0 
                    self.turn_off_all_stripled()
                
                self.hello_last_time = current_time

