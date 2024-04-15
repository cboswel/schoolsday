#!/usr/bin/env python3

from deprivation_by_postcode import *
import pandas as pd
import pgeocode
import rich_dataframe

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

def get_gender_scores(genders):
    scores = []
    for gender in genders:
        if gender == "female":
            score = 1
        elif gender == "male":
            score = -1
        else:
            score = 0
        scores.append(score)
    return scores
        
def get_type_scores(types):
    scores = []
    for school_type in types:
        if school_type == "utc":
            score = 1
        elif school_type == "private":
            score = -1
        else:
            score = 0
        scores.append(score)
    return scores

if __name__ == "__main__":

    distance_scalar = 5
    deprivation_scalar = 5
    gender_scalar = 5
    type_scalar = 5

    data = pd.read_excel("schools.xlsx")
    data["deprivation"] = get_deprivation(data["postcode"])
    data["best_distance"] = get_best_distances(data["postcode"])
    data["genders"] = get_gender_scores(data["gender"])
    data["types"] = get_type_scores(data["type"])
    data["distance_rank"] = data["best_distance"].rank()
    data["deprivation_rank"] = data["deprivation"].rank()
    data["gender_rank"] = data["genders"].rank(ascending=False)
    data["type_rank"] = data["types"].rank(ascending=False)
    distance_scaled = (data["distance_rank"] * distance_scalar)
    deprivation_scaled = (data["deprivation_rank"] * deprivation_scalar)
    gender_scaled = (data["gender_rank"] * gender_scalar)
    type_scaled = (data["type_rank"] * type_scalar)
    data["priority"] = distance_scaled + deprivation_scaled + gender_scaled + type_scaled

    table = data.sort_values("priority")
    print(rich_dataframe.prettify(table))

"""
prioritise:
    Most deprived best access. If lumping, fine.
    Location? Not very important.
    School specific: Private, school meals, type[De-prioritise independent, +UTC, +singlesex female -siglesex male, visited before?]
    Which dates do you want? (ranked)
"""
