from world.field import Field
from game.hive import Hive
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
            self.fields[x][1] = Field("water", 0, 0, "")
            self.fields[x][self._height - 1] = Field("water", 0, 0, "")
            self.fields[x][self._height - 2] = Field("water", 0, 0, "")
        for y in range(self._height):
            self.fields[0][y] = Field("water", 0, 0, "")
            self.fields[1][y] = Field("water", 0, 0, "")
            self.fields[self._width - 1][y] = Field("water", 0, 0, "")
            self.fields[self._width - 2][y] = Field("water", 0, 0, "")

        hive_positions = []
        hive_positions_dict = []
        circumference = self._width * 2 + self._height - 2 * 2
        distance = circumference // hive_count
        # Need some explanation here
        for i in range(hive_count):
            x = 0
            y = 0
            if i == 0:
                x = 2
                y = 2
            elif i == 1:
                x = 2
                y = self._height - 3
            elif i == 2:
                x = self._width - 3
                y = self._height - 3
            elif i == 3:
                x = self._width - 3
                y = 2
            else:
                if i % 4 == 0:
                    x = 2
                    y = 2 + distance * (i // 4)
                elif i % 4 == 1:
                    x = 2 + distance * (i // 4)
                    y = self._height - 3
                elif i % 4 == 2:
                    x = self._width - 3
                    y = self._height - 3 - distance * (i // 4)
                elif i % 4 == 3:
                    x = self._width - 3 - distance * (i // 4)
                    y = 2
            hive_positions.append((x, y))
            self.fields[x][y] = Field("hive", 0, 0, "")

        # Place hives on the map
        for x, y in hive_positions:
            self.fields[x][y] = Field("hive", 0, 0, "")

        # Place food in the middle of the map
        self.fields[map_size // 2][map_size // 2] = Field("food", 99, 0, "")

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
    playing_field = map.create_world(5)
    # Hive placement overflows
    print('Hive locations: \n', playing_field)
    print("----------------------------")

    print('5x5 around hive (2, 11): \n', map.show_area(2, 11, "red", 2))
    print("----------------------------")

    map_area = json.loads(map.show_map())  # Parse the JSON array into a Python list
    chunk_size = map.width
    for i in range(0, len(map_area), chunk_size):
        print(map_area[i:i + chunk_size])

