"""
La Raspberry Pi envoie un signal haut en continue sur le GPIO4  qui passe par un bouton d'arret d'urgence
vers la Carte d'alimentation 
Cette carte coupe l'alimentation de tout le système et alimente uniquement la raspberry Pi si le signal haut
ne lui parvient plus
En cas de coupure La batterie de 7.4V prend le relais pour alimenter la raspberry Pi   
"""
from gpiozero import LED



class EmergencySignal:
    def __init__(self):
        self.emergency_pin = LED(4)


    def emergencySignal(self):
        #print("gpiozero is working!")
        self.emergency_pin.on()

