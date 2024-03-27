from world.field import Field
from game.hive import Hive
import random
import json


class Map:
    """
    represents the map for the game world
    """

    def __init__(self):
        self._width = 0
        self._height = 0
        self.fields = []

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def create_world(self, hive_count: int):
        """
        creates the game world
        :param hive_count: the number of hives in the world
        :return: a list of dictionaries with the x and y coordinates of the hives
        """
        map_size = hive_count * 3 + 2
        self._width = self._height = map_size

        self.fields = [[Field("ground", 0, 0, "") for _ in range(self._height)] for _ in range(self._width)]

        for x in range(self._width):
            self.fields[x][0] = Field("water", 0, 0, "")
            self.fields[x][self._height - 1] = Field("water", 0, 0, "")
        for y in range(self._height):
            self.fields[0][y] = Field("water", 0, 0, "")
            self.fields[self._width - 1][y] = Field("water", 0, 0, "")

        hive_positions = []
        hive_positions_dict = []

        circumference = (self._width - 4) * 2 + (self._height - 6) * 2
        distance = circumference // hive_count

        # place hives:

        last_hive = [2, 2]  # self.fields[5][0] --> x: 5, y: 0
        for i in range(hive_count):
            x, y = last_hive[0], last_hive[1]

            print("Itteration: ", i)
            print("X: ", last_hive[0], "Y: ", last_hive[1])

            hive_positions.append((x, y))
            print(hive_positions)
            self.fields[x][y] = Field("hive", 0, 0, "")

            if last_hive[0] + distance < self._width - 4:
                last_hive[0] = last_hive[0] + distance
                print("1")

            elif last_hive[0] + distance > self._width - 4 and last_hive[1] + distance < self._height - 4:
                remainder = last_hive[0] + distance - (self._width - 3)
                last_hive[0] = self._width - 3
                last_hive[1] = last_hive[1] + remainder
                print("2")

            elif last_hive[1] + distance > self._height - 4 and last_hive[0] - distance < self._width - 4:
                remainder = last_hive[1] + distance - (self._height - 3)
                last_hive[1] = self._height - 3
                last_hive[0] = last_hive[0] - remainder
                print("3")

            elif last_hive[0] - distance > self._width - 4 and last_hive[1] + distance < self._height - 4:
                remainder = last_hive[0] + distance - (self._height - 3)
                last_hive[0] = self._height - 3
                last_hive[1] = last_hive[1] - distance
                print("4")

        # Calculate the starting position for the food
        if hive_count < 9:
            food = int(hive_count / 2)
        else:
            food = int(hive_count / 3)
        start_x = (self._width - food) // 2
        start_y = (self._height - food) // 2

        # Place food in the middle of the map for each hive in a rectangular pattern
        for i in range(food):
            for j in range(food):
                if j == 0 or j == food - 1:
                    self.fields[start_x + i][start_y + j] = Field("food", random.randint(1, 99), 0, "")
                elif i == 0:
                    self.fields[start_x][start_y + j] = Field("food", random.randint(1, 99), 0, "")
                elif i == food - 1:
                    self.fields[start_x + i][start_y + j] = Field("food", random.randint(1, 99), 0, "")

        for x, y in hive_positions:
            # takes x, y values from hive_positions and appends them as dictionary into hive_positions_dict
            hive_positions_dict.append({'xcoord': x, 'ycoord': y})

        return hive_positions_dict

    def show_area(self, xcoord, ycoord, color, view_range):
        """
        shows the area around a given coordinate
        :param xcoord: the x coordinate
        :param ycoord: the y coordinate
        :param color: the color of the hive
        :param view_range: the range to show around the given coordinate
        :return: a JSON array with the fields around the given coordinate
        """
        area_around = []
        for x in range(xcoord - view_range, xcoord + view_range + 1):
            for y in range(ycoord - view_range, ycoord + view_range + 1):
                if 0 <= x < self._width and 0 <= y < self._height:
                    field = self.fields[x][y]
                    match field.type:
                        case "ground":
                            area_around.append("empty")
                        case "water":
                            area_around.append("water")
                        case "hive":
                            if Hive.color == color:
                                area_around.append("home")
                            else:
                                area_around.append("hive")
                        case "food":
                            area_around.append("food")
                        case "ant":
                            """
                                In future should be able to distinguish between own and enemy ants, when that has been
                                implemented in the Ants class
                                if Ant.color == color:
                                    area_around.append("friend")
                                else:
                                    area_around.append("foe")
                            """
                            area_around.append("ant")

        if area_around[12] == "hive" or area_around[12] == "home":
            # checks if the hive is at the center of the view range
            return json.dumps(area_around)

        return 'Something went wrong!'

    def show_map(self):
        """
        shows the whole map
        :return: a JSON array with the whole map
        """
        surroundings = []
        for x in range(self._width):
            for y in range(self._height):
                field = self.fields[x][y]
                match field.type:
                    case "ground":
                        surroundings.append("empty")
                    case "water":
                        surroundings.append("water")
                    case "hive":
                        # Hive color should be added here
                        surroundings.append("hive")
                    case "food":
                        surroundings.append("food")
                    case "ant":
                        # Ant color should be added here
                        surroundings.append("ant")
        return json.dumps(surroundings)


if __name__ == '__main__':
    map = Map()
    playing_field = map.create_world(6)
    # Hive placement overflows
    print('Hive locations: \n', playing_field)
    print("----------------------------")

    print('5x5 around hive (2, 11): \n', map.show_area(2, 2, "red", 2))
    print("----------------------------")

    map_area = json.loads(map.show_map())  # Parse the JSON array into a Python list
    chunk_size = map.width
    for i in range(0, len(map_area), chunk_size):
        print(map_area[i:i + chunk_size])
