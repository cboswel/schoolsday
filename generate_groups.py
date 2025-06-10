#!/usr/bin/env python3

import random

def generate_groups(number_of_groups):
    groups = []
    for _ in range(number_of_groups):
        groups.append(random.randint(1, 40))
    return groups

if __name__ == "__main__":
    groups = generate_groups(9)
    print(groups)
