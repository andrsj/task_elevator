import logging


from elevator.functions import HouseGenerator, HouseHandler


MAX_VALUE = 5  # Can be moved to other file (like config.py or const.py) but it's not necessary
START_FLOUR = 1  # Start from first flour

logging.basicConfig(level=logging.ERROR)  # I just used only INFO logging, so...


def main():
    generator = HouseGenerator()
    flours = generator.get_flours()
    handler = HouseHandler(flours)
    handler.process()


if __name__ == '__main__':
    main()
