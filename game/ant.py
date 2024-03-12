from dataclasses import dataclass


@dataclass
class Ant:
    """
    an ant in the hive
    """
    xcoord: int
    ycoord: int
    food: int

    @property
    def xcoord(self):
        return self._xcoord

    @xcoord.setter
    def xcoord(self, value):
        self._xcoord = value

    @property
    def ycoord(self):
        return self._ycoord

    @ycoord.setter
    def ycoord(self, value):
        self._ycoord = value

    @property
    def food(self):
        return self._food

    @food.setter
    def food(self, value):
        self._food = value
