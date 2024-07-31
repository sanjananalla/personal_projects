"""This specially named module makes the package runnable."""

from exercises.ex09 import constants
from exercises.ex09.model import Model
from exercises.ex09.view_controller import ViewController


def main() -> None:
    """Entrypoint of simulation."""
    model: Model = Model(constants.CELL_COUNT, constants.CELL_SPEED, constants.CELL_INFECTED, constants.CELL_IMMUNE) # come back to last parameter 10 and figure out why only 1 ball changes color
    view_controller: ViewController = ViewController(model)
    view_controller.start_simulation()


if __name__ == "__main__":
    main()