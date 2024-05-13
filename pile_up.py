#!/usr/bin/env python3

import random
import pdb
import timeit

MAX_GROUP_SIZE = 40
MIN_GROUP_SIZE = 35
AVAILABLE_SPOTS = 16
THOROUGHNESS = 1
TEST_REPS = 250
NUMBER_OF_GROUPS = 200

class Group:
    def __init__(self, position, size, score, possible_slots):
        self.position = position
        self.size = size
        self.score = score
        self.slots = possible_slots

def generate_groups(number_of_groups):
    groups = []
    for i in range(number_of_groups):
        size = random.randint(1, MAX_GROUP_SIZE)
        score = random.randint(1, 10)
        slots = random.sample(range(16), 3)
        group = Group([i], size, score, slots)
        groups.append(group)
    return groups

def dont_skip():
    percentage_chance = 50
    if random.randint(0, 100) < percentage_chance:
        return True
    else:
        return False

def combine(groups, newGroups):
    if groups[0].size > MAX_GROUP_SIZE:
        raise Exception(f"Group of length {groups[0].size} found, groups must be under {MAX_GROUP_SIZE}.")
    totSize = 0
    totScore = 0
    places = []
    delete_pile = []
    for group in groups:
        if (dont_skip()):
            if totSize + group.size <= MAX_GROUP_SIZE:
                totSize += group.size
                totScore += group.score
                places.append(group.position)
                delete_pile.append(group)
    newGroup = Group(places, totSize, totScore)
    newGroups.append(newGroup)
    for group in delete_pile:
        groups.remove(group)
    return 0
            
def pile_up(startingGroups):
    groups = sorted(startingGroups, key=lambda x: x.size, reverse=True)
    newGroups = []
    while groups != []:
        combine(groups, newGroups)
    return newGroups

def test_once(tops):
    top_score = 0
    top_configuration = []
    startingGroups = generate_groups(NUMBER_OF_GROUPS)
    for i in range(THOROUGHNESS):
        groups = pile_up(startingGroups)
        delete_pile = []
        for group in groups:
            if group.size < MIN_GROUP_SIZE:
                delete_pile.append(group)
        for group in delete_pile:
            groups.remove(group)
        groups = sorted(groups, key=lambda x: x.score, reverse=True)
        iteration_score = 0
        for group in groups[:AVAILABLE_SPOTS]:
            iteration_score += group.score
        if iteration_score > top_score:
            top_score = iteration_score
            top_configuration = groups[:AVAILABLE_SPOTS]
    tops.append(top_score)

def test_set(tops):
    for _ in range(TEST_REPS):
        test_once(tops)
    avg = sum(tops) / len(tops)
    return avg

if __name__ == "__main__":
    tops = []
    test_once(tops)
    x = []
    y = []
    times = []
    for i in range(10, 100):
        tops = []
        THOROUGHNESS = i * 10
       # times.append(timeit.timeit("y.append(test_set(tops))", globals=globals()))
        y.append(test_set(tops))
        x.append(THOROUGHNESS)
        print(f"thoroughness of {THOROUGHNESS} yields {y[i-10]}")
    pdb.set_trace()
        
