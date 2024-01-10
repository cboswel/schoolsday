#!/usr/bin/env python3

from deprivation_by_postcode import *
import pandas as pd

class School():
    def __init__(self, name, distance, funding, students, contact="", contact_number=""):
       self.name = name
       self.distance = distance
       self.funding = funding
       self.students = students
       self.contact = contact
       self.contact_number = contact_number

if __name__ == "__main__":
    data = pd.read_excel("schools.xlsx")
    data["deprivation"] = get_deprivation(data["postcode"])
    data["distance_rank"] = data["distance"].rank()
    data["deprivation_rank"] = data["deprivation"].rank()
    data["priority"] = data["distance_rank"] + data["deprivation_rank"]
    print(data.sort_values("priority"))


"""
prioritise:
    Most deprived best access. If lumping, fine.
    Location? Not very important.
    School specific: Private, school meals, type[De-prioritise independent, +UTC, +singlesex female -siglesex male, visited before?]
    Which dates do you want? (ranked)
