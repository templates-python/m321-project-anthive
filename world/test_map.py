import pytest

from field import Field
from map import Map


def test_map():

    game_map = Map()

    # Test add_ant function
    game_map.fields = [[Field("ground", 1, 0, "") for _ in range(5)] for _ in range(5)]  # Create a 5x5 grid of fields
    game_map.add_ant(2, 2, "red")  # Add an ant at position (2, 2) with color "red"
    print(game_map.fields[2][2])
    assert 1 == game_map.fields[2][2].ants  # Check if the number of ants in the field is updated
    assert "red" == game_map.fields[2][2].hive  # Check if the color of the ant is updated

    # Test remove_ant function
    game_map.remove_ant(2, 2, "red")  # Remove the ant at position (2, 2) with color "red"
    assert game_map.fields[2][2].ants == 0  # Check if the number of ants in the field is updated

    # Test move_ant function
    game_map.add_ant(2, 2, "blue")  # Add an ant at position (2, 2) with color "blue"
    game_map.move_ant(2, 2, 3, 3)  # Move the ant from (2, 2) to (3, 3)
    assert game_map.fields[2][2].ants == 0  # Check if the number of ants in the starting field is updated
    assert game_map.fields[2][2].hive == "" # Check if color is deleted

    assert game_map.fields[3][3].ants == 1  # Check if the number of ants in the target field is updated
    assert game_map.fields[3][3].hive == "blue" # Check if color is updated


    # Test change_food function
    game_map.change_food(1, 1, 10)  # Change the amount of food at position (1, 1) to 10
    assert game_map.fields[1][1].food == 10  # Check if the amount of food in the field is updated


if __name__ == "__main__":
    test_map()
    print("All tests passed!")
