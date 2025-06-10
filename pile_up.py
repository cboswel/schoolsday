#!/usr/bin/env python3

import random
import pdb
import matplotlib.pyplot as plt

MAX_GROUP_SIZE = 40
MIN_GROUP_SIZE = 35
AVAILABLE_SPOTS = 16
THOROUGHNESS = 50000
NUMBER_OF_GROUPS = 200

class Group:
    def __init__(self, position, size, score, possible_slots):
        self.position = position
        self.size = size
        self.score = score
        self.slots = possible_slots

class Board:
    def __init__(self, sizes):
        self.remainings = list(sizes)
        self.groups = [[] for _ in range(len(self.remainings))]
        self.score = 0

def generate_groups(number_of_groups):
    groups = []
    for i in range(number_of_groups):
        size = random.randint(5, MAX_GROUP_SIZE)
        score = random.randint(1, 10)
        slots = random.sample(range(AVAILABLE_SPOTS), 3)
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
        if group.size > MAX_GROUP_SIZE:
            raise Exception(f"Group of length {groups[0].size} found, groups must be under {MAX_GROUP_SIZE}.")
        if dont_skip():
            max_slot = 0
            for slot in group.slots:
                if board.remainings[slot] > max_slot:
                    max_slot = slot
            slot = max_slot
            if board.remainings[slot] >= group.size:
                board.remainings[slot] -= group.size
                board.score += group.score
                board.groups[slot].append(group.size)
            delete_pile.append(group)
    for group in delete_pile:
        groups.remove(group)
    return 0

def pile_up(startingGroups):
    board = Board([MAX_GROUP_SIZE] * AVAILABLE_SPOTS)
    groups = sorted(startingGroups, key=lambda x: x.score, reverse=True)
    while groups != []:
        combine(groups, board)
    enriched_kids = 0
    for group in board.groups:
        enriched_kids += sum(group)
    board.score = board.score * enriched_kids
    return board

def test_once():
    startingGroups = generate_groups(NUMBER_OF_GROUPS)
    best_board = Board([0])
    for i in range(THOROUGHNESS):
        board = pile_up(startingGroups)
        if board.score > best_board.score:
            best_board = board
    return best_board

# TODO: Make it so it doesn't error when there's an empty slot. Instead, try other configurations first. Score it so an empty slot adds zero - that way that configuarion is probably skipped.
def test_set(end):
    global THOROUGHNESS
    results = []
    while THOROUGHNESS < end:
        board = test_once()
        results.append(board.score)
        THOROUGHNESS += 1
        print(THOROUGHNESS)
    x = range(len(results))
    y = results
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()

if __name__ == "__main__":
    board = test_once()
    for group in board.groups:
        print(sum(group))
    pdb.set_trace()

