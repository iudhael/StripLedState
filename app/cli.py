import typer
from typing_extensions import Annotated
from ledsignalisation.addr_stripled_signalisation_non_bloquant_V2 import AddrStripLedSignalisationNonBloquant2
from emergencysignalisation.emergency_signal import EmergencySignal
from audio.speaker import Speaker
from audio.microphone import Microphone


app = typer.Typer(
    name="signal",
    help="Interface CLI pour les composants de signalisation (LEDs, Audio, Urgence).",
    no_args_is_help=True,
)

# --- Fonction utilitaire pour initialiser les LEDs ---
# Nous initialisons les objets une seule fois ou dans la fonction pour être sûr qu'ils existent
def get_leds():
    """Initialise et retourne l'objet de contrôle des LEDs non bloquantes."""
    try:
        
        return AddrStripLedSignalisationNonBloquant2()
    except Exception as e:
        typer.echo(f"Erreur d'initialisation des LEDs : {e}", err=True)
        raise typer.Exit(1)

# --- Commande pour les LEDs de statut (ready, danger, etc.) ---
@app.command()
def status_led(
    status: Annotated[
        str,
        typer.Argument(help="Statut à afficher : ready, danger, booting, hello")
    ],
) -> None:
    """Affiche un statut prédéfini sur la bande LED."""
    leds = get_leds()

    if status.lower() == "ready":
        leds.ready()
    elif status.lower() == "danger":
        leds.danger()
    elif status.lower() == "booting":
        leds.booting()
    elif status.lower() == "hello":
        leds.hello()
    else:
        typer.echo(f"Erreur : Statut '{status}' non reconnu.", err=True)
        raise typer.Exit(1)
        
    typer.echo(f"Affichage du statut '{status}'.")

# --- Commande pour l'indicateur de direction (turn) ---
@app.command()
def turn_signal(
    direction: Annotated[
        str,
        typer.Argument(help="Direction du clignotement : droite ou gauche")
    ],
) -> None:
    """Affiche un clignotant de direction sur la bande LED."""
    leds = get_leds()
    
    if direction.lower() in ["droite", "gauche"]:
        leds.turn(direction=direction.lower())
        typer.echo(f"Activation du clignotant '{direction}'.")
    else:
        typer.echo("Erreur : La direction doit être 'droite' ou 'gauche'.", err=True)
        raise typer.Exit(1)

# --- Commande pour le signal d'urgence ---
@app.command()
def emergency() -> None:
    """Active le signal d'arrêt d'urgence."""
    try:
        EmergencySignal().emergencySignal()
        typer.echo("Signal d'arrêt d'urgence activé.")
    except Exception as e:
        typer.echo(f"Erreur lors de l'activation du signal d'urgence : {e}", err=True)
        raise typer.Exit(1)

# --- Commande pour le son (Exemple) ---
@app.command()
def play_sound(
    file: Annotated[str, typer.Argument(help="Chemin du fichier audio à jouer")],
) -> None:
    """Joue un fichier audio via le haut-parleur."""
    try:
        speaker = Speaker()
        typer.echo(f"Lecture du fichier : {file} (Non implémenté dans le corps de la fonction, mais l'objet est initialisé).")
        # Ici, vous ajouteriez l'appel à la méthode pour jouer le son
        # speaker.play(file) 
    except Exception as e:
        typer.echo(f"Erreur lors de l'initialisation du haut-parleur : {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()