"""

    https://core-electronics.com.au/guides/raspberry-pi/fully-addressable-rgb-raspberry-pi/


    sudo pip3 install rpi_ws281x
    sudo pip3 install adafruit-circuitpython-neopixel
    sudo python3 -m pip install --force-reinstall adafruit-blinka

    Controle de 6 segments de  stripled sans delay avec un seul GPIO de la raspberry Pi
    Chaque méthode détermine un état du robot (hello, booting, danger, ready, turn...)
    
    on s'assure d'éteindre toutes les leds avec self.turning_off_all_stripled()
    avant d'appeler un autre service d'état ros
    


    #include all neccessary packages to get LEDs to work with Raspberry Pi

"""

import time
import board
import neopixel


NEOPIXEL_PIN = board.D12

class AddrStripLedSignalisationNonBloquantV2:
    def __init__(self, nbre_led_par_segment = 10):
        """
            Chaque segment (gauche, droite, milieu) à 10 leds
        """
        self.nbre_led_par_segment = nbre_led_par_segment 
        self.nbre_led_total = 6 * self.nbre_led_par_segment  # 60 LEDs
        #self.global_brightness = 1

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
        self.pre_operational_last_time = 0
        self.pre_operational_stripled_is_on = False
        self.pre_operational_fading_laste_time = 0
        self.pre_operational_fading_brightness = 0

        self.ready_last_time = 0
        self.ready_stripled_is_on = False

        self.emergency_stop_last_time = 0
        self.emergency_stop_stripled_is_on = False

        self.ready_to_go_last_time = 0

        self.turning_last_time = 0
        self.turning_stripled_is_on = False

        self.braking_last_time = 0

        self.reverse_last_time = 0
        self.reverse_index = 0
        
        self.hello_last_time = 0
        self.hello_step = 0 
        self.hello_index = 0
        self.hello_color_index = 0
        self.hello_start = 0 

        """ Couleurs off """
        self.off = (0, 0, 0)
        """ rouge, vert, bleu, orange, blanc"""
        self.color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 165, 0), (255, 255, 255)]

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
        
    """
    Remplit un segment spécifique de la bande avec une couleur,
    en appliquant un niveau de brillance sur le segment.
    """
    def fill_segment(self, start, end, color_rgb, segment_brightness=1.0):        
        # S'assurer que la brillance est dans la plage [0.0, 1.0]
        segment_brightness = max(0.0, min(1.0, segment_brightness))
        
        # Extraire les composantes de la couleur de base
        r, g, b = color_rgb
        
        # Calculer la nouvelle couleur atténuée
        r_final = int(r * segment_brightness)
        g_final = int(g * segment_brightness)
        b_final = int(b * segment_brightness)
        
        final_color = (r_final, g_final, b_final)

        for i in range(start, end):
            self.all_stripled[i] = final_color
            
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

    """
    Pre-Operational (Initialization)
    All LEDs (front & rear): Blue
    Animation: Breathing pattern at ~0.5 Hz
    Purpose: Indicates system power-on and initialization phase.

    """
    def pre_operational(self):
        """print("pre_operational ...")"""
        current_time = time.time()

        if self.pre_operational_fading_brightness  <= 1 and self.pre_operational_stripled_is_on == False:
                       
            if current_time - self.pre_operational_fading_laste_time >= 0.01:
                
                self.fill_segment(self.start_front_middle, self.end_front_middle, self.color[2], self.pre_operational_fading_brightness) # blue
                self.fill_segment(self.start_back_middle, self.end_back_middle, self.color[2], self.pre_operational_fading_brightness) # blue
                
                self.fill_segment(self.start_front_left, self.end_front_left, self.color[2], self.pre_operational_fading_brightness) # blue
                self.fill_segment(self.start_front_right, self.end_front_right, self.color[2], self.pre_operational_fading_brightness) # blue

                self.fill_segment(self.start_back_left, self.end_back_left, self.color[2], self.pre_operational_fading_brightness) # blue
                self.fill_segment(self.start_back_right, self.end_back_right, self.color[2], self.pre_operational_fading_brightness) # blue
            
            self.pre_operational_fading_brightness += 0.01
            
            #print(self.pre_operational_fading_brightness)
            if self.pre_operational_fading_brightness >=  1:
                self.pre_operational_stripled_is_on = True
                
                
            self.pre_operational_last_time = current_time 

        if self.pre_operational_fading_brightness  >= 0 and self.pre_operational_stripled_is_on == True:
            if current_time - self.pre_operational_fading_laste_time >= 0.01:
            
                self.fill_segment(self.start_front_middle, self.end_front_middle, self.color[2], self.pre_operational_fading_brightness) # blue
                self.fill_segment(self.start_back_middle, self.end_back_middle, self.color[2], self.pre_operational_fading_brightness) # blue
                
                self.fill_segment(self.start_front_left, self.end_front_left, self.color[2], self.pre_operational_fading_brightness) # blue
                self.fill_segment(self.start_front_right, self.end_front_right, self.color[2], self.pre_operational_fading_brightness) # blue

                self.fill_segment(self.start_back_left, self.end_back_left, self.color[2], self.pre_operational_fading_brightness) # blue
                self.fill_segment(self.start_back_right, self.end_back_right, self.color[2], self.pre_operational_fading_brightness) # blue
            
            self.pre_operational_fading_brightness -= 0.01
            #print(self.pre_operational_fading_brightness)
            
            if self.pre_operational_fading_brightness <=  0:
                self.pre_operational_stripled_is_on = False
            self.pre_operational_last_time = current_time

    """
    Ready (Idle, Motion Enabled)
    All LEDs (front & rear): Green
    Animation: Simple 1 Hz blink (synchronized across all lights)
    Purpose: Robot is enabled and awaiting motion commands.

    """
    def ready(self):
        """print("ready...")"""
        current_time = time.time()
        if current_time - self.ready_last_time >= 0.5:
            if self.ready_stripled_is_on == False:
                self.all_stripled.fill(self.color[1]) # vert
                self.ready_stripled_is_on = True
            else:
                self.all_stripled.fill(self.off) # Éteint
                self.ready_stripled_is_on = False
            
            self.all_stripled.show()
            self.ready_last_time = current_time

    """Clignotement simple de toutes les LEDs en rouge"""
    def emergency_stop(self):
        """print("emergency_stop ...")"""
        current_time = time.time()
        if current_time - self.emergency_stop_last_time >= 0.25:
            if self.emergency_stop_stripled_is_on == False:
                self.all_stripled.fill(self.color[0]) # Rouge
                self.emergency_stop_stripled_is_on = True
            else:
                self.all_stripled.fill(self.off)
                self.emergency_stop_stripled_is_on = False

            self.all_stripled.show()
            self.emergency_stop_last_time = current_time


    """
    Element                     Behavior        Color
    Center LEDs (front & rear)  Solid           Green
    Front side LEDs             Headlights      White steady
    Rear side LEDs              Taillights      Dim red steady
    """
    
    def ready_to_go(self, segment_brightness = 0.05):
        """print("ready to go...")"""
        current_time = time.time()
        if current_time - self.ready_to_go_last_time >= 0.5:
            self.fill_segment(self.start_front_middle, self.end_front_middle, self.color[1]) # vert
            self.fill_segment(self.start_back_middle, self.end_back_middle, self.color[1]) # vert
            
            self.fill_segment(self.start_front_left, self.end_front_left, self.color[4]) # blanc
            self.fill_segment(self.start_front_right, self.end_front_right, self.color[4]) # blanc

            self.fill_segment(self.start_back_left, self.end_back_left, self.color[0], segment_brightness) # rouge faible
            self.fill_segment(self.start_back_right, self.end_back_right, self.color[0], segment_brightness) # rouge faible

            self.ready_to_go_last_time = current_time
        
            
    """
    Turn Signal
    Corresponding side LEDs on both front and rear bumpers sweep blink yellow.
    Sweep direction: inward to center on both bumpers.
    Blink rate: 1 Hz.
    
    
    """
    def turning(self, direction, segment_brightness = 0.05):
        """print(f"turn... {direction}")"""
        current_time = time.time()

        s_front, e_front, s_back, e_back = self.get_segment_indices(direction)

        start_front = s_front + 2
        end_front = e_front - 2 
        start_back = s_back + 2
        end_back = e_back - 2 
        
        """garde les leds du millieu allumées"""
        self.fill_segment(self.start_front_middle, self.end_front_middle, self.color[1]) # vert
        self.fill_segment(self.start_back_middle, self.end_back_middle, self.color[1]) # vert


        if direction != "gauche":
            
            self.fill_segment(self.start_front_left, self.end_front_left, self.color[4]) # blanc
            self.fill_segment(self.start_back_left, self.end_back_left, self.color[0], segment_brightness) # rouge faible

        if direction != "droite":
            
            self.fill_segment(self.start_front_right, self.end_front_right, self.color[4]) # blanc
            self.fill_segment(self.start_back_right, self.end_back_right, self.color[0], segment_brightness) # rouge faible

        
        """allumer les deux premieres et dernieres led """
        led = 2
        self.fill_segment(s_front, s_front + led, self.color[4], segment_brightness) # blanc faible
        self.fill_segment(e_front - led, e_front, self.color[4], segment_brightness) # blanc faible
        
        self.fill_segment(s_back, s_back + led, self.color[0], segment_brightness) # rouge faible
        self.fill_segment(e_back - led, e_back, self.color[0], segment_brightness) # rouge faible

        if current_time - self.turning_last_time >= 0.25:
            if self.turning_stripled_is_on == False:
                self.fill_segment(start_front, end_front, self.color[3])
                self.fill_segment(start_back, end_back, self.color[3])
                self.turning_stripled_is_on = True
            else:
                self.fill_segment(start_front, end_front, self.off)
                self.fill_segment(start_back, end_back, self.off)
                self.turning_stripled_is_on = False

            self.all_stripled.show()
            self.turning_last_time = current_time

    """
    Braking
    Rear side LEDs: Bright red steady while braking.
    """
    def braking(self):
        """print("braking...")"""
        current_time = time.time()
        if current_time - self.braking_last_time >= 0.5:
            self.fill_segment(self.start_front_middle, self.end_front_middle, self.color[1]) # vert
            self.fill_segment(self.start_back_middle, self.end_back_middle, self.color[1]) # vert
            
            self.fill_segment(self.start_front_left, self.end_front_left, self.color[4]) # blanc
            self.fill_segment(self.start_front_right, self.end_front_right, self.color[4]) # blanc

            self.fill_segment(self.start_back_left, self.end_back_left, self.color[0]) # rouge vif
            self.fill_segment(self.start_back_right, self.end_back_right, self.color[0]) # rouge vif

            self.braking_last_time = current_time

    """
    Reverse
    Rear side LEDs: Outer half of each side LED strip switches to white steady.
    Remaining LEDs retain normal taillight behavior (dim red).

    """
    def reverse(self, segment_brightness = 0.05):
        current_time = time.time()
        if current_time - self.ready_last_time >= 0.5:
            self.fill_segment(self.start_front_middle, self.end_front_middle, self.color[1]) # vert
            self.fill_segment(self.start_back_middle, self.end_back_middle, self.color[1]) # vert
            
            self.fill_segment(self.start_front_left, self.end_front_left, self.color[4]) # blanc
            self.fill_segment(self.start_front_right, self.end_front_right, self.color[4]) # blanc

            half_segment = int(self.nbre_led_par_segment/2)
            self.fill_segment(self.start_back_left, self.start_back_left + half_segment, self.color[4]) # blanc vif
            self.fill_segment(self.start_back_right, self.start_back_right + half_segment, self.color[0]) # rouge faible

            self.fill_segment(self.start_back_left + half_segment , self.end_back_left , self.color[0], segment_brightness) # rouge faible
            self.fill_segment(self.start_back_right + half_segment, self.end_back_right , self.color[4], segment_brightness) # blanc vif



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
                
        if self.hello_step == 6 and current_time - self.hello_last_time >= 0.2:
                """ ÉTAPE 6 : Fenêtre de 3 LEDs qui défilent """
                window_size = 3
                if self.hello_start <= (self.nbre_led_par_segment - window_size):
                    # Éteindre avant de défiler
                    self.turn_off_all_stripled()

                    """ Allumer la fenêtre de 3 LEDs """
                    for i in range(window_size):
                        self.all_stripled[self.start_front_middle + self.hello_start + i] = self.color[2]
                        self.all_stripled[self.start_back_middle + self.hello_start + i] = self.color[2]
                        
                        self.all_stripled[self.start_front_left + self.hello_start + i] = self.color[2]
                        self.all_stripled[self.start_back_left + self.hello_start + i] = self.color[2]

                        self.all_stripled[self.start_front_right + self.hello_start + i] = self.color[2]
                        self.all_stripled[self.start_back_right + self.hello_start + i] = self.color[2]
                        
                    self.all_stripled.show()
                    self.hello_start += 1
                else:
                    self.turn_off_all_stripled()
                    self.hello_index = 0
                    self.hello_start = 0
                    self.hello_step += 1
                    
                self.hello_last_time = current_time


        """ Séquence d'allumage progressif en arc-en-ciel (rainbow-like) """
        if self.hello_step == 7:
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

