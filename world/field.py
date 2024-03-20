from dataclasses import dataclass


@dataclass
class Field:
    """
    represents one field of the game world
    """
    type: str  # the field type "ground", "water", "hive"
    food: int  # the amount of food on this field
    ants: int  # the number of ants on this field
    hive: str  # the hive color the ants belong to

