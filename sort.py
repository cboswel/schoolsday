#!/usr/bin/env python3

#from deprivation_by_postcode import *
import pandas as pd
import pgeocode
import pdb
import random

#TODO: Types are backwardsly sorted, weightings? CSV output. Infinite score?

MAX_GROUP_SIZE = 42
MIN_GROUP_SIZE = 35
AVAILABLE_SPOTS = 16
THOROUGHNESS = 10000000

class Group:
    def __init__(self, size, score, possible_slots, name, email, postcode, types):
        self.size = size
        self.score = score
        self.slots = possible_slots
        self.name = name
        self.assigned_slot = None
        self.email = email
        self.postcode = postcode
        self.types = types

class Board:
    def __init__(self, dates):
        self.remainings = {}
        self.sizes = {}
        self.groups = []
        for date in dates:
            self.remainings[date] = MAX_GROUP_SIZE
            self.sizes[date] = []
        self.score = 0

def get_best_distances(postcodes):
    STEP_postcode = "DN22"
    FTF_postcode = "S60"
    Culham_postcode = "OX14"

    STEP_distances = []
    FTF_distances = []
    Culham_distances = []

    distance_rating_STEP = 5;
    distance_rating_Culham = 5;
    distance_rating_FTF = 5;
    dist = pgeocode.GeoDistance('GB')
    for postcode in postcodes:
        STEP_distances.append(dist.query_postal_code(postcode, STEP_postcode))
        FTF_distances.append(dist.query_postal_code(postcode, FTF_postcode))
        Culham_distances.append(dist.query_postal_code(postcode, Culham_postcode))

    best_scores = []
    for i, _ in enumerate(postcodes):
        best = max(STEP_distances[i] * distance_rating_STEP,
                    FTF_distances[i] * distance_rating_FTF,
                    Culham_distances[i] * distance_rating_Culham)
        best_scores.append(best)
    return best_scores

def get_gender_scores(types):
    scores = []
    for gender in types:
        if "boys" in gender:
            score = 1
        elif "girls" in gender:
            score = -1
        else:
            score = 0
        scores.append(score)
    return scores

def get_type_scores(types, names):
    scores = []
    for i, school_type in enumerate(types):
        if "UTC" in school_type or "UTC" in names[i]:
            score = -1
        elif "Independent" in school_type:
            score = 1
        else:
            score = 0
        #print(f"{school_type} given a score of {score}")
        scores.append(score)
    return scores

def FSM_scores(FSM):
    scores = []
    for percentage in FSM:
        percentage = str(percentage).replace("%", "")
        if percentage == '?':
            scores.append(0)
        else:
            try:
                percentage = float(percentage)
            except:
                print(f"Bad data point {percentage} in FSM")
            if percentage > 40:
                score = 40
            elif percentage < 10:
                score = 0
            else:
                score = percentage
            score = len(FSM) - ((score / 40) * len(FSM)) # get a score out of <number of schools>
            scores.append(score)
    return scores

def possible_date(dates):
    slots = []
    for date in dates:
        if date not in slots:
            slots.append(date)
    return slots

def date_parse(dates):
    date_list = []
    for date in dates:
        if date[-1] == ";":
            date = date[:-1]
        date_list.append(date.split(";"))
    return date_list

def dont_skip():
    percentage_chance = 50
    if random.randint(0, 100) < percentage_chance:
        return True
    else:
        return False

def combine(groups, board):
    delete_pile = []
    for group in groups:
        if group.size > MAX_GROUP_SIZE:
            raise Exception(f"Group of length {groups[0].size} found, groups must be under {MAX_GROUP_SIZE}.")
        if dont_skip():
            max_remaining = 0
            best_slot = group.slots[0]
            for slot in group.slots:
                if board.remainings[slot] > max_remaining:
                    max_remaining = board.remainings[slot]
                    best_slot = slot
            slot = best_slot
            if board.remainings[slot] >= group.size:
                board.remainings[slot] -= group.size
                board.score += group.score
                board.sizes[slot].append(group.size)
                group.assigned_slot = slot
                board.groups.append(group)
            delete_pile.append(group)
    for group in delete_pile:
        groups.remove(group)
    return 0

def pile_up(startingGroups, board):
    groups = sorted(startingGroups, key=lambda x: x.score, reverse=True)
    while groups != []:
        combine(groups, board)
    enriched_kids = 0
    for date in board.sizes.values():
        enriched_kids += sum(date)
    board.score = board.score * enriched_kids
    if board.score == 'inf':
        pdb.set_trace()
    return board

def test_once():
    startingGroups = generate_groups(NUMBER_OF_GROUPS)
    best_board = Board([0])
    for i in range(THOROUGHNESS):
        board = pile_up(startingGroups)
        if board.score > best_board.score:
            best_board = board
    return best_board


if __name__ == "__main__":
    data = pd.read_excel("data.xlsx")
#    data["deprivation"] = get_deprivation(data["postcode"])
    data["best_distance"] = get_best_distances(data["postcode"])
    data["genders"] = get_gender_scores(data["type"])
    data["types"] = get_type_scores(data["type"], data["name"])
    data["distance_rank"] = data["best_distance"].rank()
    data["FSM_scores"] = FSM_scores(data["FSM"])
#    data["deprivation_rank"] = data["deprivation"].rank()
    data["gender_rank"] = data["genders"].rank(ascending=False)
    data["type_rank"] = data["types"].rank(ascending=False)
    deprivation_scaled = 1
    data["priority"] = data["distance_rank"] + data["FSM_scores"] + data["type_rank"] + data["gender_rank"] # + data["deprivation_rank"]
    data["dates"] = date_parse(data["dates"])
    #pdb.set_trace()
    """
    print("type:")
    print(data.sort_values("type_rank")[["name", "type", "type_rank"]])
    print("gender:")
    print(data.sort_values("gender_rank")[["name", "type", "gender_rank"]])
    print("FSM:")
    print(data.sort_values("FSM_scores")[["name", "FSM", "FSM_scores"]])
    """
    data = data.sort_values("priority")
    #print(data[["name", "distance_rank", "priority", "type_rank", "gender_rank"]])

    groups = []
    for index, group in data.iterrows():
        try:
            int(group["priority"])
        except:
            pdb.set_trace()
        groups.append(Group(group["numbers"], group["priority"], group["dates"], group["name"], group["email"], group["postcode"], group["type"]))
    possible_dates = []
    for date_list in data["dates"]:
        for date in date_list:
            if date not in possible_dates:
                possible_dates.append(date)
    board = Board(possible_dates)

    best_board = Board(["1st Jan"])
    for i in range(THOROUGHNESS):
        new_board = pile_up(groups, board)
        if new_board.score > best_board.score:
            best_board = new_board


    output_data = {"name" : [], "size" : [], "email" : [], "postcode" : [], "assigned_slot" : []}
    cut_data = {"name" : [], "type" : [], "size" : [], "email" : [], "postcode" : []}
    for group in best_board.groups:
        if group.name not in output_data["name"]:
            output_data["name"].append(group.name)
            output_data["size"].append(group.size)
            output_data["email"].append(group.email)
            output_data["postcode"].append(group.postcode)
            output_data["assigned_slot"].append(group.assigned_slot)

    df =  pd.DataFrame(output_data)
    df = df.sort_values("assigned_slot")
    name_list = []
    for name in df["name"]:
        name_list.append(name)
    for index, group in data.iterrows():
        if group["name"] not in name_list:
            cut_data["name"].append(group["name"])
            cut_data["size"].append(group["numbers"])
            cut_data["email"].append(group["email"])
            cut_data["postcode"].append(group["postcode"])
            cut_data["type"].append(group["type"])
    cut_df = pd.DataFrame(cut_data)
    df.to_csv('out.csv', index=False)
    cut_df.to_csv('rej.csv', index=False)


"""
prioritise:
    Most deprived best access. If lumping, fine.
    Location? Not very important.
    School specific: Private, school meals, type[De-prioritise independent, +UTC, +singlesex female -siglesex male, visited before?]
    Which dates do you want? (ranked)
"""
