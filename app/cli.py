import typer
from typing_extensions import Annotated
from ledsignalisation.addr_stripled_signalisation_non_bloquant_V2 import AddrStripLedSignalisationNonBloquantV2

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
        
        return AddrStripLedSignalisationNonBloquantV2()
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

    if status.lower() == "pre_operational":
        leds.pre_operational()
    elif status.lower() == "ready":
        leds.ready()
    elif status.lower() == "emergency_stop":
        leds.emergency_stop()
    elif status.lower() == "ready_to_go":
        leds.ready_to_go()
    elif status.lower() == "braking":
        leds.braking()
    elif status.lower() == "reverse":
        leds.reverse()
    elif status.lower() == "hello":
        leds.hello()
    elif status.lower() == "turn_off_all_stripled":
        leds.turn_off_all_stripled()
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
        leds.turning(direction=direction.lower())
        typer.echo(f"Activation du clignotant '{direction}'.")
    else:
        typer.echo("Erreur : La direction doit être 'droite' ou 'gauche'.", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()