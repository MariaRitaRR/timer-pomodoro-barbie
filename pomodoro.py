from time import monotonic

from textual.app import App, ComposeResult
from textual.widgets import Digits, Button, Static
from textual.containers import Container
from textual.reactive import reactive

import random

CARACTERES = ["✧", "✦", "♡", "⋆", "˚", "·", "❀"]
class Timedisplay(Digits):
    """A widget para mostrar o tempo restante"""
    start_time = reactive(0.0)
    total = reactive(1500.0)
    time = reactive(1500.0)
    running = reactive(False)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.timer = self.set_interval(1, self.update_time, pause=True) ## faz nascer parado
        
    def update_time(self) -> None:
        """Method to update the time to the current time."""
        decorrido = monotonic() - self.start_time
        restante = self.total - decorrido
        if restante <= 0:
            self.reset()
        else:
            self.time = restante

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        self.update(f"{minutes:02.0f}:{seconds:02.0f}")

    def start(self):
        self.start_time = monotonic()
        self.timer.resume()
        self.running = True


    def stop(self):
        self.timer.pause()
        self.running = False

    def reset(self):
        self.timer.pause()
        self.time = self.total
        self.running = False
        self.app.query_one(BotaoStart).update("Iniciar")

class BotaoStart(Static):
    def on_click(self) -> None:
        display = self.app.query_one(Timedisplay)
        if not display.running:
            display.start()
            self.update("Pausar")
        else:
            display.stop()
            self.update("Iniciar")

class Sparkle(Static):
    cores = ["#ff8fcf", "#c77dff", "#ffb6d9", "#ff5fa2"]
    indice = reactive(0)

    def __init__(self, char: str):
        super().__init__(char)
        self.char = char

    def on_mount(self) -> None:
        self.set_interval(random.uniform(0.3, 1.2), self.piscar)

    def piscar(self) -> None:
        self.indice = (self.indice + 1) % len(self.cores)

    def watch_indice(self, indice: int) -> None:
        self.styles.color = self.cores[indice]
        self.update(self.char)
class Pomodoro(App):
    CSS_PATH = "pomodoro.tcss"

    def compose(self) -> ComposeResult:
        for i in range(100):
            char = random.choice(CARACTERES)
            sparkle = Sparkle(char)
            sparkle.styles.layer = "fundo"
            sparkle.styles.offset = (
                random.randint(-50, 50),
                random.randint(-1, 1),
            )
            yield sparkle
        yield Container(
            Timedisplay(),
            BotaoStart("Iniciar", id="start"),
        )

if __name__ == "__main__":
    Pomodoro().run()