from world.field import Field


class Map:
    """
    represents the map for the game world
    """

    def __init__(self):
        self._width = 0
        self._height = 0
        self.fields = []

    def create_world(self, hive_count):

        map_size = hive_count * 3 + 2
        self._width = map_size
        self._height = map_size

        self.fields = [[Field("ground", 0, 0, "") for _ in range(self._height)] for _ in range(self._width)]

        for x in range(self._width):
            self.fields[x][0] = Field("water", 0, 0, "")
            self.fields[x][self._height - 1] = Field("water", 0, 0, "")
        for y in range(self._height):
            self.fields[0][y] = Field("water", 0, 0, "")
            self.fields[self._width - 1][y] = Field("water", 0, 0, "")

        hive_positions = []
        circumference = self._width * 2 + self._height - 2 * 2
        distance = circumference // hive_count
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

        for x, y in hive_positions:
            self.fields[x][y] = Field("hive", 0, 0, "")

        self.fields[map_size // 2][map_size // 2] = Field("food", 99, 0, "")

        return hive_positions

    def show_area(self, xcoord, ycoord, color, view_range):

        area_around = []
        for x in range(xcoord - view_range, xcoord + view_range + 1):
            for y in range(ycoord - view_range, ycoord + view_range + 1):
                if 0 <= x < self._width and 0 <= y < self._height:
                    field = self.fields[x][y]
                    if field.type == "ground":
                        area_around.append("empty")
                    elif field.type == "water":
                        area_around.append("water")
                    elif field.type == "hive":
                        area_around.append("hill")
                    elif field.type == "food":
                        area_around.append("food")
        return area_around

    def show_map(self):

        surroundings = []
        for x in range(self._width):
            for y in range(self._height):
                field = self.fields[x][y]
                if field.type == "ground":
                    surroundings.append("empty")
                elif field.type == "water":
                    surroundings.append("water")
                elif field.type == "hive":
                    surroundings.append("hive")
                elif field.type == "food":
                    surroundings.append("food")
        return surroundings


if __name__ == '__main__':
    map = Map()
    map.create_world(5)

    area = map.show_area(2, 2, "red", 2)

    map_area = map.show_map()

    print(area)
    print("----------------------------")
    chunk_size = map._width
    for i in range(0, len(map_area), chunk_size):
        print(map_area[i:i + chunk_size])

