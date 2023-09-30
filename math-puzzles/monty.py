"""
Monty Hall Problem

* There are 3 doors. One luxury car behind one of them and the others have 2 goat behind.
* If the Challenger open correct door of the car, it will belong to the challenger.
* After the challenger choose one door, the Host who knows correct answer will open one of the left door which has goat.
* Then the host will ask the challenger whether likes to reselect the door ?
* Should the Challenger keep first choice? or change the other one? which has high possibility?
"""

import random
import logging


def play_monty_game(is_challenger_reselect: bool) -> str:
    """
    play one round of the monty game
    """
    logging.debug("--------------game start-------------------")
    door_with_car_ind: int = dice(3)
    doors: [] = setup_doors(door_with_car_ind)
    logging.debug("1. Car behind the [%s] door.", door_with_car_ind + 1)
    logging.debug("1. Doors: %s.", doors)

    challenger_choose_door_ind: int = dice(3)
    doors[challenger_choose_door_ind][2] = None  # host cannot open
    logging.debug("2. Challenger choose the [%s] door.", challenger_choose_door_ind + 1)
    logging.debug("2. Doors: %s.", doors)

    host_open_door_ind: int = host_choose_door_to_open(doors)
    doors[host_open_door_ind][2] = None
    doors[host_open_door_ind][3] = None  # challenger cannot reselect anymore
    logging.debug("3. Host choose the [%s] door.", host_open_door_ind + 1)
    logging.debug("3. Doors: %s.", doors)

    if is_challenger_reselect:
        challenger_choose_door_ind = challenger_reselect_door_to_open(challenger_choose_door_ind, doors)
    logging.debug("4. Challenger will reselect? %s.", is_challenger_reselect)
    logging.debug("4. Challenger finally choose the [%s] door.", challenger_choose_door_ind + 1)
    logging.debug("4. Doors: %s.", doors)

    logging.debug("================game stop==================")
    if challenger_choose_door_ind == door_with_car_ind:
        return 'win'
    else:
        return 'loose'


def dice(total_num: int) -> int:
    """
    Mimic dice, given random number 0, 1, 2
    """
    return random.randint(0, total_num - 1)


def setup_doors(door_with_car_ind: int) -> []:
    """
    Store array [index, item_name, host_can_open, challenger_can_choose]
    """
    doors: [] = [[1, 'goat', True, True], [2, 'goat', True, True], [3, 'goat', True, True]]
    doors[door_with_car_ind] = [door_with_car_ind + 1, 'car', None, True]
    return doors


def host_choose_door_to_open(doors: []) -> int:
    host_available_doors: [] = [door for door in doors if door[2]]
    if len(host_available_doors) == 1:
        return host_available_doors[0][0] - 1
    else:
        host_open_door_ind: int = dice(2)
        return host_available_doors[host_open_door_ind][0] - 1


def challenger_reselect_door_to_open(previous_ind: int, doors: []) -> int:
    challenger_available_doors: [] = [door for door in doors if door[3]]
    if int(challenger_available_doors[0][0]) - 1 == previous_ind:
        return challenger_available_doors[1][0] - 1
    else:
        return challenger_available_doors[0][0] - 1


def test(is_challenger_reselect: bool, times: int) -> []:
    results: [] = [['win', 0], ['loose', 0]]
    for i in range(times):
        result = play_monty_game(is_challenger_reselect)
        if 'win' == result:
            results[0][1] += 1
        else:
            results[1][1] += 1
    return results


logging.root.setLevel(logging.DEBUG)
total_game_round = 1000
result_no_reselect = test(False, total_game_round)
print('result_no_reselect:', result_no_reselect)

result_with_reselect = test(True, total_game_round)
print('result_with_reselect:', result_with_reselect)
