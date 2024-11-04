import json
import pandas as pd
import pandas as pd
import sys
from scipy.spatial import cKDTree
from shapely.geometry import Point


with open("listed_buildings.geojson") as f:
    data = json.load(f)

df = pd.DataFrame(data["features"])


# Extract coordinates and Name into a new DataFrame
new_df = pd.DataFrame(
    {
        "lon": df["geometry"].apply(lambda x: x["coordinates"][0][0]),
        "lat": df["geometry"].apply(lambda x: x["coordinates"][0][1]),
        "Name": df["properties"].apply(lambda x: x["Name"]),
        "Listdate": df["properties"].apply(lambda x: x["ListDate"]),
        "Grade": df["properties"].apply(lambda x: x["Grade"]),
        "hyperlink": df["properties"].apply(lambda x: x["hyperlink"]),
    }
)


if sys.argv[1] == str(1):
    new_df = new_df[new_df["Grade"] == 'I']
elif sys.argv[1] == str(2):
    new_df = new_df[new_df["Grade"] == "II"]
elif sys.argv[1] == str(22):
    new_df = new_df[new_df["Grade"] == "II*"]
else:
    None

# Convert longitude and latitude into a list of tuples
points = list(zip(new_df["lon"], new_df["lat"]))
print(new_df.head(5))


# Build a cKDTree with these points
tree = cKDTree(points)

# Input point (longitude, latitude) for which we want the nearest point
input_point = (-0.0954023, 51.5609817)

# Query the tree to find the nearest point
distance, index = tree.query(input_point)

# Get the nearest point's coordinates and the distance to the input point
nearest_point = points[index]
nearest_distance = distance

print(
    f"Nearest Listed building to {input_point} is the grade {new_df['Grade'].loc[index]} listed {new_df['Name'].loc[index]} at location {nearest_point} with a distance of {nearest_distance:.4f}"
)


# save the processed data

print(new_df.to_csv("processed.csv"))
