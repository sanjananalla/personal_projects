"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from random import random
from exercises.ex09 import constants
from math import sin, cos, pi, sqrt


__author__ = "730573834"


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def distance(self, other: Point) -> float:
        """Calculates the distance between two points."""
        change_in_x: float = self.x - other.x
        change_in_y: float = self.y - other.y
        dist_val: float = sqrt(change_in_x**2 + change_in_y**2)
        return dist_val


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE

    def contract_disease(self) -> None:
        """Cell becomes infected and assigned a value of 1."""
        self.sickness = constants.INFECTED

    def is_vulnerable(self) -> bool:
        """Checks if the value of sickness is equal to 0 which would signify if the cell is vulnerable or not and returns a bool value."""
        if (self.sickness == 0):
            return True
        else:
            return False

    def is_infected(self) -> bool:
        """Checks if sickness value is equal to or greater than 1 which would signify the cell is infected and returns bool value."""
        if (self.sickness >= 1):
            return True
        else:
            return False

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    # Part 1) Define a method named `tick` with no parameters.
    # Its purpose is to reassign the object's location attribute
    # the result of adding the self object's location with its
    # direction. Hint: Look at the add method.

    def tick(self) -> None:
        """Alters cells to become immune if the cell has been infected longer than the recovery period."""
        self.location = self.location.add(self.direction)
        if (self.is_infected()):
            self.sickness += 1
            if (self.sickness == constants.RECOVERY_PERIOD):
                self.immunize()    

    def color(self) -> str:
        """Return the color representation of a cell."""
        if (self.is_vulnerable() is True):
            return "gray"
        if (self.is_infected() is True):
            return "red"
        if (self.is_immune() is True):
            return "black"

    def contact_with(self, other: Cell) -> None:
        """If a infected cell comes in contact with a vulnerable cell, the vulnerable cell becomes infected as well."""
        if (self.is_infected() is True and other.is_vulnerable() is True):
            other.contract_disease()
        elif (self.is_vulnerable() is True and other.is_infected() is True):
            self.contract_disease()

    def immunize(self) -> None:
        """Make cell immune and assign value of -1."""
        self.sickness = constants.IMMUNE

    def is_immune(self) -> bool:
        """Check if cell is immune or equal to -1."""
        if (self.sickness == -1):
            return True
        else:
            return False
    

class Model:
    """The state of the simulation."""

    population: list[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, infected_cells: int, immune_cells: int = 0):
        """Initialize the cells with random locations and directions."""
        self.population = []
        if (infected_cells >= cells):
            raise ValueError("Number of infected cells should be some proportion of all cells, but not equal to all cells.")
        if (infected_cells <= 0):
            raise ValueError("Some number of infected cells must exist.")
        if (immune_cells >= cells):
            raise ValueError("Number of immune cells should be less than the number of total cells.")
        if (immune_cells < 0):
            raise ValueError("sdfkhsadbf")
        if ((immune_cells + infected_cells) >= cells):
            raise ValueError("The total number of immune and infected cells should not be larger than the number of total cells in the simulation.")
        
        for _ in range(cells):
            start_location: Point = self.random_location()
            start_direction: Point = self.random_direction(speed)
            cell: Cell = Cell(start_location, start_direction)
            self.population.append(cell)
        for i in range(infected_cells):
            self.population[i].contract_disease()
        for i in range(immune_cells):
            self.population[i].immunize()

    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x: float = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y: float = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle: float = 2.0 * pi * random()
        direction_x: float = cos(random_angle) * speed
        direction_y: float = sin(random_angle) * speed
        return Point(direction_x, direction_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if (cell.location.x > constants.MAX_X):
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1.0
        if (cell.location.x < constants.MIN_X):
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1.0
        if (cell.location.y > constants.MAX_Y):
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1.0
        if (cell.location.y < constants.MIN_Y):
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1.0

    def check_contacts(self) -> None:
        """Checks if any cell is in contact with another cell without repeating cells and if two cells are closer than the set cell radius and if one cell is infected while the other isn't, the vulnerable cell becomes infected."""
        for i in range(0, len(self.population)):
            for j in range(i + 1, len(self.population)):
                if (self.population[i].location.distance(self.population[j].location) < constants.CELL_RADIUS):
                    self.population[i].contact_with(self.population[j])
                    
    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        for cell in self.population:
            if cell.is_infected():
                return False
        return True
