#!/usr/bin/env python3

from deprivation_by_postcode import *
import pandas as pd
import pgeocode
import pdb
import random

class Group:
    def __init__(self, size, score, possible_slots, name, email, postcode, types):
        self.score = score
        self.name = name
        self.email = email
        self.postcode = postcode
        self.types = types

class Board:
    def __init__(self, dates):
        self.remainings = {}
        self.score = 0

def get_best_distances(postcodes):
    STEP_postcode = "DN22"
    FTF_postcode = "S60"
    Culham_postcode = "OX14"
    RAICo_postcode = "CA28"

    STEP_distances = []
    FTF_distances = []
    Culham_distances = []
    RAICo_distances = []

    distance_rating_STEP = 5
    distance_rating_Culham = 5
    distance_rating_FTF = 5
    distance_rating_RC = 5
    dist = pgeocode.GeoDistance('GB')
    for postcode in postcodes:
        STEP_distances.append(dist.query_postal_code(postcode, STEP_postcode))
        FTF_distances.append(dist.query_postal_code(postcode, FTF_postcode))
        Culham_distances.append(dist.query_postal_code(postcode, Culham_postcode))
        RAICo_distances.append(dist.query_postal_code(postcode, RAICo_postcode))

    best_scores = []
    for i, _ in enumerate(postcodes):
        best = min(STEP_distances[i] * distance_rating_STEP,
                    FTF_distances[i] * distance_rating_FTF,
                    Culham_distances[i] * distance_rating_Culham,
                   RAICo_distances[i] * distance_rating_RC)
        best_scores.append(best)
        if best != best:
            pdb.set_trace()

    return best_scores

def get_gender_scores(types):
    scores = []
    for gender in types:
        if "boys" in gender:
            score = -1
        elif "girls" in gender:
            score = 1
        else:
            score = 0
        scores.append(score)
    return scores

def get_type_scores(types, names):
    scores = []
    for i, school_type in enumerate(types):
        if "UTC" in school_type or "UTC" in names[i]:
            score = 1
        elif "Independent" in school_type:
            score = -1
        else:
            score = 0

        """
        REMOVING TYPE SCORES THIS YEAR
        """

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

if __name__ == "__main__":
    data = pd.read_excel("data.xlsx")
    data["deprivation"] = get_deprivation(data["postcode"])
    data["best_distance"] = get_best_distances(data["postcode"])
    data["genders"] = get_gender_scores(data["type"])
    data["types"] = get_type_scores(data["type"], data["name"])
    data["distance_rank"] = data["best_distance"].rank()
    data["FSM_scores"] = FSM_scores(data["FSM"])
    data["deprivation_rank"] = data["deprivation"].rank()
    data["gender_rank"] = data["genders"].rank(ascending=False)
    data["type_rank"] = data["types"].rank(ascending=False)
    deprivation_scaled = 1
    data["priority"] = data["distance_rank"] + data["FSM_scores"] * 1.2 + data["type_rank"] + data["gender_rank"] # + data["deprivation_rank"]
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
    print(data[["name", "priority", "distance_rank", "type_rank", "gender_rank", "FSM_scores", "deprivation_rank"]][:12])
    print(data[["name"]][:12])

    """
    output_data = {"name" : [], "size" : [], "email" : [], "postcode" : [], "assigned_slot" : []}
    cut_data = {"name" : [], "type" : [], "size" : [], "email" : [], "postcode" : []}
        if group.name not in output_data["name"]:
            output_data["name"].append(group.name)
            output_data["size"].append(group.size)
            output_data["email"].append(group.email)
            output_data["postcode"].append(group.postcode)

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
