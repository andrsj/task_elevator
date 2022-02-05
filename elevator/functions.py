# MAIN LOGIC

from random import randint
import logging

from elevator.types import Elevator, Person, Flour, Direction
from elevator.utils import get_another_flour


class HouseGenerator:
    """Generator of flours and people who are included in specific flour"""
    def __init__(self):
        self.flour_count = randint(5, 20)

    def get_flours(self):
        return self._generate_flours()

    def _generate_flours(self) -> tuple[Flour]:
        flours = tuple(
            Flour(value=i, people=self._generate_people_for_flour(i))
            for i in range(1, self.flour_count + 1)
        )
        return flours

    def _generate_people_for_flour(self, flour_value: int) -> list[Person]:
        people_count = randint(0, 10)
        people = []
        for _ in range(people_count):
            end = get_another_flour(self.flour_count, flour_value)
            person = Person(
                flour_value=flour_value,
                end_flour_value=end,
            )
            people.append(person)

        return people


class HouseHandler:
    """Main process of house elevator"""

    def __init__(self, flours: tuple[Flour]):
        self.flours = flours
        self.elevator = Elevator(Direction.UP, 1)

    def process(self):
        current_flour = 1
        counter = 0  # For step display

        print("Plz note, the structure is demonstrated before processing")

        # Infinity loop for process
        # Because we update person direction, when he leave elevator
        #                                  or when he enter to endpoint flour
        #                                  [it's the same value XD]
        while True:
            # Be attention!
            input()  # PAUSE PROGRAM
            # Be attention!

            print(f'Step {counter}')
            self.show()

            flour = self.flours[current_flour - 1]  # Can be spec method :)
            self.process_exit_elevator(flour)
            self.process_enter_elevator(flour)

            self.check_changing_direction(flour)

            current_flour += self.elevator.direction.value  # Changing local counter for looping between flour
            counter += 1  # For step

    def check_changing_direction(self, fl: Flour):

        # Max flour bound
        if fl.value == len(self.flours):
            self.elevator.reverse_direction()

        # Min flour bound
        elif fl.value == 1:
            self.elevator.reverse_direction()

        # The need to keep moving
        if not self.elevator.is_empty():

            # Calculate max need flour value
            # and depends on result - choose need direction
            if self.elevator.direction == Direction.UP:
                max_flour = max((p.end_flour_value for p in self.elevator.people))
                if max_flour < self.elevator.flour_value:
                    self.elevator.reverse_direction()
            elif self.elevator.direction == Direction.DOWN:
                min_flour = min((p.end_flour_value for p in self.elevator.people))
                if min_flour > self.elevator.flour_value:
                    self.elevator.reverse_direction()
        else:

            # If elevator empty
            # then check if there are people
            # on the next flours
            next_flours = filter(
                lambda v: v.value < fl.value
                if self.elevator.direction == Direction.DOWN
                else v.value > fl.value,
                self.flours
            )
            count_people = sum(len(flour) for flour in next_flours)
            if not count_people:
                self.elevator.reverse_direction()

        self.process_enter_elevator(fl)
        self.elevator.flour_value += self.elevator.direction.value

    def process_exit_elevator(self, fl: Flour):
        """ [elevator] -> [flour ##] """
        pr = "[EXIT] "
        logging.info(pr + 'Check if elevator empty')
        if self.elevator.is_empty():
            return
        logging.info(pr + f'Exit people [el] v -> #{fl.value}[]')
        people = self.elevator.get_people_from_elevator_by_flour(fl.value)
        logging.info(pr + 'Enter people [el] -> v #{fl.value}[]')
        for person in people:
            logging.info(pr + f'Updating person, old: {person}')
            person.update_person(fl.value, get_another_flour(len(self.flours), fl.value))
            logging.info(pr + f'Updated person, new: {person}')
            fl.add_person(person)

    def process_enter_elevator(self, fl: Flour):
        """ [elevator] <- [flour ##] """
        pr = "[ENTER] "
        logging.info(pr + 'Check if flour empty')
        if fl.is_empty():
            return
        logging.info(pr + 'Pushing to elevator people')
        while len(self.elevator) < 5:
            logging.info(pr + f'Getting person {self.elevator}')
            person = fl.pop_person_by_direction(self.elevator.direction)
            logging.info(pr + f'Person: {person}')
            if person is None:
                logging.info(pr + 'No person, go next flour')
                break
            logging.info(pr + 'Pushing to elevator')
            self.elevator.push_people_to_elevator(person)

    def show(self):
        for flour in reversed(self.flours):
            if self.elevator.flour_value == flour.value:
                el = str(self.elevator)
            else:
                el = ''
            print('|{} {:<30}| {}'.format(flour.value, el, flour))
