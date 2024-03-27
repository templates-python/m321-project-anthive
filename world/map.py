import json
from world.field import Field


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

    
    def show_area(self, xcoord, ycoord, color, viewrange):
        ant_coord = (xcoord, ycoord)
        coordList = []
        for y in range(ycoord + viewrange, ycoord - viewrange - 1, -1):
            for x in range(xcoord - viewrange, xcoord + viewrange + 1):
                if (x, y) != ant_coord:
                    fieldType = Field.type
                    match fieldType:
                        case "ground":
                            if Field.food > 0:
                                coordList.append({'x-coordination': x, 'y-coordination': y, 'state': 'food'})
                            elif Field.ants > 0:
                                if Field.hive == color:
                                    coordList.append({'x-coordination': x, 'y-coordination': y, 'state': "friend"})
                                else:
                                    coordList.append({'x-coordination': x, 'y-coordination': y, 'state': "foe"})
                            else:
                                coordList.append({'x-coordination': x, 'y-coordination': y, 'state': 'empty'})
                        case "water":
                            coordList.append({'x-coordination': x, 'y-coordination': y, 'state': 'water'})
                        case "hive":
                            if Field.hive == color:
                                coordList.append({'x-coordination': x, 'y-coordination': y, 'state': 'home'})
                            else:                                
                                coordList.append({'x-coordination': x, 'y-coordination': y, 'state': 'hill'})
        return json.dumps(coordList)
    
    def show_map():
        worldmap = []
        fieldType = Field.type
        for y in range(self._height, -1):
            for x in range(self._width):
                match fieldType:
                    case "hive":
                        worldmap.append({'x-coordination': x, 'y-coordination': y, 'state': Field.hive})
                    case "water":
                        worldmap.append({'x-coordination': x, 'y-coordination': y, 'state': 'water'})
                    case "ground":
                        if Field.food > 0:
                            worldmap.append({'x-coordination': x, 'y-coordination': y, 'state': 'food'})
                        elif Field.ants > 0:
                            worldmap.append({'x-coordination': x, 'y-coordination': y, 'state': Field.hive})
                        else:
                            worldmap.append({'x-coordination': x, 'y-coordination': y, 'state': 'empty'})
        return json.dumps(worldmap)
    