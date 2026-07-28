from time import monotonic

from textual.app import App, ComposeResult
from textual.widgets import Digits, Button
from textual.containers import Container
from textual.reactive import reactive

class Timedisplay(Digits):
    """A widget para mostrar o tempo restante"""
    start_time = reactive(monotonic)
    time = reactive(1500.0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.set_interval(1 / 60, self.update_time)

    def update_time(self) -> None:
        """Method to update the time to the current time."""
        decorrido = monotonic() - self.start_time
        self.time = time - decorrido

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        self.update(f"{minutes:02.0f}:{seconds:05.2f}")


class Pomodoro(App):
    CSS_PATH = "pomodoro.tcss"

    def compose(self) -> ComposeResult:
        yield Container(

            Button("Iniciar", id="start"),
            Timedisplay()
        )

if __name__ == "__main__":
    Pomodoro().run()