
class Map:
    """
    represents the map for the game world
    """

    def __init__(self):
        self._width = 0
        self._height = 0
        self.fields = []


    def add_ant(self, xcoord, ycoord, color):
        """
        add ant with the given color
        :return:
        """
        field = self.fields[xcoord][ycoord]
        print(field)
        field.ants += 1
        field.hive = color

    def remove_ant(self, xcoord, ycoord, color):
        """
        remove ant
        :return:
        """
        field = self.fields[xcoord][ycoord]
        print(field)
        field.ants -= 1
        field.hive = ""

    def move_ant(self, xcoord_start, ycoord_start, xcoord_target, ycoord_target):
        """
        move ant
        :return: type of field ['food', 'water', etc.]
        """
        old_field = self.fields[xcoord_start][ycoord_start]
        old_field.ants -= 1

        new_field = self.fields[xcoord_target][ycoord_target]
        new_field.ants += 1
        new_field.hive = old_field.hive
        print(f" new field: {new_field}")
        old_field.hive = ""
        print(f" old field: {old_field}")

        return new_field.type

    def change_food(self, xcoord, ycoord, amount):
        """
        change amount of food on a field
        :return:
        """
        field = self.fields[xcoord][ycoord]
        field.food = amount
        print(field)
