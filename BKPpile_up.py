#!/usr/bin/env python3

import random
import pdb
import timeit

MAX_GROUP_SIZE = 40
MIN_GROUP_SIZE = 35
AVAILABLE_SPOTS = 8
THOROUGHNESS = 1
TEST_REPS = 250
NUMBER_OF_GROUPS = 200

class Group:
    def __init__(self, position, size, score, possible_slots):
        self.position = position
        self.size = size
        self.score = score
        self.slots = possible_slots

class Board:
    def __init__(self, sizes):
        self.remainings = remainings
        self.groups = [[] * len(remainings)]
        self.score = 0

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
"""
def combine(groups, newGroups):
    if groups[0].size > MAX_GROUP_SIZE:
        raise Exception(f"Group of length {groups[0].size} found, groups must be under {MAX_GROUP_SIZE}.")
    slot = groups[0].slots[0]
    totSize = 0
    totScore = 0
    places = []
    delete_pile = []
    for group in groups:
        if dont_skip() and slot in group.slots:
            if totSize + group.size <= MAX_GROUP_SIZE:
                totSize += group.size
                totScore += group.score
                places.append(group.position)
                delete_pile.append(group)
    newGroup = Group(places, totSize, totScore, slot)
    newGroups.append(newGroup)
    for group in delete_pile:
        groups.remove(group)
    return 0
"""
def combine(groups, board):
    delete_pile = []
    for group in groups:
        if groups[0].size > MAX_GROUP_SIZE:
            raise Exception(f"Group of length {groups[0].size} found, groups must be under {MAX_GROUP_SIZE}.")
        if dont_skip():
            slot = max(board.remainings[group.slots])
            if board.remainings[slot] >= group.size:
                board.remainings[slot] -= group.size
                board.score += group.score
                delete_pile.append(group)
    for group in delete_pile:
        groups.remove(group)
    return 0
            
def pile_up(startingGroups):
    board = Board([40] * AVAILABLE_SPOTS)
    groups = sorted(startingGroups, key=lambda x: x.score, reverse=True)
    while groups != []:
        combine(groups, board)
    return board

def test_once(tops):
    top_score = 0
    top_configuration = []
    startingGroups = generate_groups(NUMBER_OF_GROUPS)
    for i in range(THOROUGHNESS):
        board = pile_up(startingGroups)
        delete_pile = []
        for leftover in board.remainings:
            if leftover > (MIN_GROUP_SIZE):
                delete_pile.append(group)
        for group in delete_pile:
            groups.remove(group)
        groups = sorted(groups, key=lambda x: x.score, reverse=True)
        iteration_score = 0
        for slot in range(AVAILABLE_SPOTS):
            slot_scores = []
            for group in groups:
                if slot == group.slots:
                    slot_scores.append(group.score)
                  #  print(f"potential group of {group.size}")
            print(f"slot {slot} score = {max(slot_scores)} and ")
            iteration_score += max(slot_scores)
            if iteration_score > top_score:
                top_score = iteration_score
                tops.append(top_score)


# TODO: Make it so it doesn't error when there's an empty slot. Instead, try other configurations first. Score it so an empty slot adds zero - that way that configuarion is probably skipped.
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
        
