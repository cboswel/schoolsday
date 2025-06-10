#!/usr/bin/env python3

def get_deprivation(postcodes):
    import pandas as pd

    req_cols = ["pcds", "lsoa11cd"]
    LSOAs = []
    deprivation_ranks = []
    data = pd.read_csv("postcodes/postcode_lookup.zip", usecols=req_cols, compression="zip", encoding='latin-1')
    for postcode in postcodes:
        index = data.loc[data["pcds"] == postcode].index[0]
        LSOA = data._get_value(index, "lsoa11cd")
        LSOAs.append(LSOA)

    for LSOA in LSOAs:
        # If we want to be fast we should do each of the countries in groups instead, to minimize file opening
        # Here's the lazy version, though:
        if LSOA[0] == "E":
            data = pd.read_csv("postcodes/england.csv")
            location = "LSOA code (2011)"
            rank = "Index of Multiple Deprivation (IMD) Rank (where 1 is most deprived)"
        elif LSOA[0] == "W":
            data = pd.read_csv("postcodes/wales.csv")
            location = "LSOA_Code"
            rank = "WIMD2019_Rank"
        elif LSOA[0] == "S":
            data = pd.read_csv("postcodes/scotland.csv")
            location = "Data_Zone"
            rank = "SIMD2020v2_Rank"
        elif LSOA[0] == "N":
            data = pd.read_csv("postcodes/ireland.csv")
            location = "LGD2014code"
            rank = "MDM_rank"
        else:
            raise Exception(f"LSOA code {LSOA} not recognised!")

        total = len(data.index)
        index = data.loc[data[location] == LSOA].index[0]
        deprivation_rank = data._get_value(index, rank)
        percentage = deprivation_rank * 100 / total
        deprivation_ranks.append(percentage)
    return deprivation_ranks

if __name__ == "__main__":
    postcodes = ["SA9 2JJ"]
    ranks = get_deprivation(postcodes)
    for _ in range(0, len(postcodes)):
        ranks[_] = "%.2f" % ranks[_]
        print(f"{postcodes[_]} is ranked in the {ranks[_]}% most deprived areas of the country!")
