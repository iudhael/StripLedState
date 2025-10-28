# Aide générale
python cli.py --help


# Aide pour une commande spécifique (ex: status-led)
python cli.py status-led --help
    


# Format général des commandes
python cli.py COMMANDE [ARGUMENTS]


# Afficher le statut 'prêt' (ready)
python cli.py status-led ready

# Afficher le statut de danger
python cli.py status-led danger

# Afficher l'animation de démarrage
python cli.py status-led booting


|Argument|Description|Valeurs Possibles|
|status|Le nom du statut prédéfini à afficher.|"ready, danger, booting, hello"|

# Clignotant pour la direction droite
python cli.py turn-signal droite

# Clignotant pour la direction gauche
python cli.py turn-signal gauche

# Active les mécanismes d'urgence (LEDs/son/arrêt, selon l'implémentation)
python cli.py emergency


# Jouer un son situé à un chemin spécifique
python cli.py play-sound /home/user/sons/alarme.wav



