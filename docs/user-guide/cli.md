# Aide générale
python signal_cli.py --help

# Aide pour une commande spécifique (ex: status-led)
python signal_cli.py status-led --help

# Format général des commandes
python signal_cli.py COMMANDE [ARGUMENTS]


# Afficher le statut 'prêt' (ready)
python signal_cli.py status-led ready

# Afficher le statut de danger
python signal_cli.py status-led danger

# Afficher l'animation de démarrage
python signal_cli.py status-led booting


|Argument|Description|Valeurs Possibles|
|status|Le nom du statut prédéfini à afficher.|"ready, danger, booting, hello"|

# Clignotant pour la direction droite
python signal_cli.py turn-signal droite

# Clignotant pour la direction gauche
python signal_cli.py turn-signal gauche

# Active les mécanismes d'urgence (LEDs/son/arrêt, selon l'implémentation)
python signal_cli.py emergency


# Jouer un son situé à un chemin spécifique
python signal_cli.py play-sound /home/user/sons/alarme.wav



