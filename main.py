import logging


from elevator.functions import HouseGenerator, HouseHandler


MAX_VALUE = 5
START_FLOUR = 1

logging.basicConfig(level=logging.ERROR)


def main():
    generator = HouseGenerator()
    flours = generator.get_flours()
    handler = HouseHandler(flours)
    handler.process()


if __name__ == '__main__':
    main()
