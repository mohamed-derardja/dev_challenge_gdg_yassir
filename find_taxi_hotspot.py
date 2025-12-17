import pandas as pd
from collections import defaultdict

#loading data + data cleaning
try:
    df = pd.read_csv("C:\\Documents\\taxi_hotspot_dataset (1).csv")
except FileNotFoundError:
    # Try alternative path
    df = pd.read_csv("taxi_hotspot_dataset (1).csv")
df = df.dropna(subset=["lat", "lon", "timestamp", "fare", "car_id"])
#converting timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])

KEY = 2017 #yassir founding year 
df["real_fare"] = df["fare"] - KEY


def is_valid_cluster(t1, t2, t3):
    A = t1["real_fare"]
    B = t2["real_fare"]
    C = t3["real_fare"]

    #rule 1 : 3 taxis diff 
    if len({t1["car_id"], t2["car_id"], t3["car_id"]}) != 3:
        return False

    #rule 2 : la formule citee 
    if round(B, 5) != round(abs(A - C) + (A % C), 5):
        return False

    return True


#process each location
location_stats = defaultdict(lambda: {
    "score": 0,
    "earliest": None,
    "lat": None,
    "lon": None
})

#implicitement on check if its the same destination (ml rules)
for (lat, lon), group in df.groupby(["lat", "lon"]):
    group = group.sort_values("timestamp")
    trips = group.to_dict("records")

    if len(trips) < 3:
        continue

    #overlap (4)
    i = 0
    while i <= len(trips) - 3:
        t1, t2, t3 = trips[i], trips[i+1], trips[i+2]

        if is_valid_cluster(t1, t2, t3):
            cluster_score = (
                t1["real_fare"] +
                t2["real_fare"] +
                t3["real_fare"]
            )

            location_stats[(lat, lon)]["score"] += cluster_score
            location_stats[(lat, lon)]["lat"] = lat
            location_stats[(lat, lon)]["lon"] = lon

            if (
                location_stats[(lat, lon)]["earliest"] is None
                or t1["timestamp"] < location_stats[(lat, lon)]["earliest"]
            ):
                location_stats[(lat, lon)]["earliest"] = t1["timestamp"]

            i += 3
        else:
            i += 1


#in case a location has score = 0
valid_locations = [
    v for v in location_stats.values() if v["earliest"] is not None
]

#tuple comparisonfor for the tie cases
if not valid_locations:
    raise ValueError("No valid hotspot found")

hotspot = max(
    valid_locations,
    key=lambda x: (
        x["score"],
        -x["earliest"].timestamp(),
        x["lat"],
        x["lon"]
    )
)

print("HOTSPOT FOUND :")
print(f"latitude: {hotspot['lat']}")
print(f"longitude: {hotspot['lon']}")
print(f"total Score: {hotspot['score']}")
print(f"earliest cluster: {hotspot['earliest']}")
print("----------------------------------")