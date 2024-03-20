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
    
