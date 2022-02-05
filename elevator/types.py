# MAIN TYPES OF ALL PROJECTS

from enum import Enum
from typing import Optional


class Direction(Enum):
    DOWN = -1
    ZERO_VALUE = 0
    UP = 1


class DirectionObject:
    _direction: Direction = Direction.ZERO_VALUE

    @property
    def direction(self) -> Direction:
        return self._direction

    def get_direction_symbol(self):
        if self._direction == Direction.UP:
            return '^'
        elif self._direction == Direction.DOWN:
            return 'v'
        else:
            # WE NEED TO SET UP DIRECTION WHILE INIT!
            raise ValueError("Zero direction is not supported")


class Person(DirectionObject):
    def __init__(self, flour_value: int, end_flour_value: int):
        self.flour_value = flour_value
        self.end_flour_value = end_flour_value
        self.update_direction()

    def __str__(self):
        return self.get_direction_symbol() + f'{self.end_flour_value}'

    def update_person(self, new_current_flour: int, new_end_point_flour: int):
        """This method usually use for regenerate direction"""
        self.flour_value = new_current_flour
        self.end_flour_value = new_end_point_flour
        self.update_direction()

    def update_direction(self):
        if self.flour_value < self.end_flour_value:
            self._direction = Direction.UP
        elif self.flour_value > self.end_flour_value:
            self._direction = Direction.DOWN
        else:
            raise ValueError("Zero direction is not supported")


class Flour:

    def __init__(self, value: int, people: list[Person]):
        self.value = value
        self.people = people

    def __len__(self):
        """len -> how many people on flour"""
        return len(self.people)

    def __str__(self):
        return f'#{self.value} [' + ' '.join(str(p) for p in self.people) + ']'

    def is_empty(self) -> bool:
        return not len(self.people)

    def add_person(self, person: Person):
        if not isinstance(person, Person):
            raise TypeError("Wrong object! We can't push not a person to flour")
        self.people.append(person)

    def pop_person_by_direction(self, direction: Direction) -> Optional[Person]:
        if not self.people:
            return
        if not [person for person in self.people if person.direction == direction]:
            return
        person = next(filter(lambda p: p.direction == direction, self.people))
        self.people.remove(person)
        return person


class Elevator(DirectionObject):
    MAX_VALUE: int = 5

    def __init__(self, direction: Direction, current_flour: int):
        self._direction = direction
        self.flour_value = current_flour
        self.people: list[Person] = []

    def is_full(self) -> bool:
        return len(self.people) == self.MAX_VALUE

    def is_empty(self) -> bool:
        return not len(self.people)

    def __len__(self):
        """len -> how many people in elevator"""
        return len(self.people)

    def push_people_to_elevator(self, person: Person):
        if self.is_full():
            raise ValueError("Can't push person in elevator")
        elif not isinstance(person, Person):
            raise TypeError("Wrong object! We can't push not a person to elevator")
        self.people.append(person)

    def get_people_from_elevator_by_flour(self, current_flour) -> list[Person]:
        people: list[Person] = list(filter(lambda p: p.end_flour_value == current_flour, self.people))
        for person in people:
            self.people.remove(person)
        return people

    def __str__(self):
        return f'({self.get_direction_symbol()}) [' + \
               ' '.join(str(person) for person in self.people) + ']'

    def reverse_direction(self):
        if self.direction == Direction.UP:
            self._direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            self._direction = Direction.UP
        else:
            raise ValueError("Can't reverse direction for ZERO VALUE direction")
