#!/usr/bin/env python3

import random
from operator import itemgetter
import pdb

MAX_GROUP_SIZE = 40

def generate_groups(number_of_groups):
    groups = []
    for i in range(number_of_groups):
        groups.append({'place' : i, 'size' : random.randint(1, MAX_GROUP_SIZE)})
    return groups

def combine(groups, newGroups):
    if groups[0]['size'] > MAX_GROUP_SIZE:
        raise Exception(f"Group of length {groups[0]['size']} found, groups must be under {MAX_GROUP_SIZE}.")
    total = 0
    places = []
    delete_pile = []
    for group in groups:
        if total + group['size'] <= MAX_GROUP_SIZE:
            total += group['size']
            places.append(group['place'])
            delete_pile.append(group)
    newGroups.append({'size' : total, 'places' : places})
    for group in delete_pile:
        groups.remove(group)
    return groups
            
def pile_up(groups):
    groups = sorted(groups, key=itemgetter('size'), reverse=True)
    newGroups = []
    while True:
        groups = combine(groups, newGroups)
        total = 0
        for group in groups:
            total += group['size']
        if total <= MAX_GROUP_SIZE:
            combine(groups, newGroups)
            break

    return newGroups

if __name__ == "__main__":
    for i in range(1):
        groups = generate_groups(30)
        groups = pile_up(groups)
        groups = sorted(groups, key=itemgetter('size'), reverse=True)
        print(groups[:10])
