# Taxi Hotspot Hunt - FINAL SOLUTION
import pandas as pd
from collections import defaultdict

FILE_PATH = r"C:\Users\mihiderar\OneDrive\Documents\CHALLENGE_DEV_GDG_Solution.xlsx"

# Decryption key found after analysis
DECRYPTION_KEY = 3200

def validate_fare_pattern(fare_a, fare_b, fare_c):
    """Check if middle fare B follows: B = |A - C| + (A mod C)"""
    try:
        A = int(fare_a)
        B = int(fare_b)
        C = int(fare_c)
        if C == 0:
            return False
        expected_B = abs(A - C) + (A % C)
        return B == expected_B
    except:
        return False

def load_and_decrypt_data(filepath, key):
    """Load Excel file and decrypt fares"""
    df = pd.read_excel(filepath)
    print(f"Total rows loaded: {len(df)}")
    
    # Clean data
    df = df.dropna(subset=['lat', 'lon', 'timestamp', 'fare', 'car_id']).copy()
    print(f"Valid rows after removing NaN: {len(df)}")
    
    # Decrypt fares
    df['original_fare'] = df['fare']
    df['fare'] = df['fare'] - key
    df = df[df['fare'] > 0]
    print(f"Rows after decryption (key={key}): {len(df)}")
    
    # Round coordinates
    df['lat'] = df['lat'].round(6)
    df['lon'] = df['lon'].round(6)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

def find_valid_clusters(df):
    """Find all valid 3-trip clusters at each location"""
    clusters_by_location = defaultdict(list)
    
    for (lat, lon), group in df.groupby(['lat', 'lon']):
        # Only Algeria coordinates (roughly 18-38°N, -9-12°E)
        if not (18 <= lat <= 38 and -9 <= lon <= 12):
            continue
        
        trips = group.sort_values('timestamp').reset_index(drop=True)
        
        for i in range(len(trips) - 2):
            trip1 = trips.iloc[i]
            trip2 = trips.iloc[i + 1]
            trip3 = trips.iloc[i + 2]
            
            # Rule 1: Different taxis
            car_ids = {trip1['car_id'], trip2['car_id'], trip3['car_id']}
            if len(car_ids) != 3:
                continue
            
            # Rule 2: Fare pattern validation
            if not validate_fare_pattern(trip1['fare'], trip2['fare'], trip3['fare']):
                continue
            
            # Valid cluster found!
            signature = int(trip1['fare'] + trip2['fare'] + trip3['fare'])
            cluster_info = {
                'fares': (int(trip1['fare']), int(trip2['fare']), int(trip3['fare'])),
                'original_fares': (int(trip1['original_fare']), int(trip2['original_fare']), int(trip3['original_fare'])),
                'signature': signature,
                'first_timestamp': trip1['timestamp'],
                'car_ids': (trip1['car_id'], trip2['car_id'], trip3['car_id'])
            }
            clusters_by_location[(lat, lon)].append(cluster_info)
    
    return clusters_by_location

def calculate_scores(clusters_by_location):
    """Calculate total score for each location"""
    scores = {}
    
    for location, clusters in clusters_by_location.items():
        total_score = sum(c['signature'] for c in clusters)
        earliest_time = min(c['first_timestamp'] for c in clusters)
        
        scores[location] = {
            'total_score': total_score,
            'num_clusters': len(clusters),
            'earliest_time': earliest_time,
            'clusters': clusters
        }
    
    return scores

def find_hotspot(scores):
    """Apply tie-breaking rules to find the hotspot"""
    if not scores:
        return None
    
    # Sort by: highest score, earliest time, largest lat, largest lon
    sorted_locations = sorted(
        scores.items(),
        key=lambda x: (
            -x[1]['total_score'],
            x[1]['earliest_time'],
            -x[0][0],
            -x[0][1]
        )
    )
    
    hotspot_location, hotspot_data = sorted_locations[0]
    return hotspot_location, hotspot_data

def main():
    print("=" * 80)
    print("🚀 TAXI HOTSPOT HUNT - FINAL SOLUTION")
    print("=" * 80)
    
    # Load and decrypt data
    print(f"\n📂 Loading data from: {FILE_PATH}")
    df = load_and_decrypt_data(FILE_PATH, DECRYPTION_KEY)
    
    # Find clusters
    print("\n🔍 Searching for valid clusters...")
    clusters_by_location = find_valid_clusters(df)
    total_clusters = sum(len(v) for v in clusters_by_location.values())
    print(f"✓ Found {total_clusters} valid clusters across {len(clusters_by_location)} locations")
    
    # Calculate scores
    print("\n💎 Calculating scores...")
    scores = calculate_scores(clusters_by_location)
    
    # Find hotspot
    print("\n🎯 Determining hotspot with tie-breaking rules...")
    result = find_hotspot(scores)
    
    if result is None:
        print("❌ No valid clusters found!")
        return
    
    hotspot_coords, hotspot_info = result
    lat, lon = hotspot_coords
    
    print("\n" + "=" * 80)
    print("✨ HOTSPOT FOUND!")
    print("=" * 80)
    print(f"\n📍 Coordinates: ({lat}, {lon})")
    print(f"💰 Total Score: {hotspot_info['total_score']}")
    print(f"🔢 Number of Valid Clusters: {hotspot_info['num_clusters']}")
    print(f"⏰ Earliest Cluster: {hotspot_info['earliest_time']}")
    print(f"🔑 Decryption Key Used: {DECRYPTION_KEY}")
    
    print(f"\n📋 Cluster Details:")
    for i, cluster in enumerate(hotspot_info['clusters'], 1):
        print(f"  {i}. Cars: {cluster['car_ids']}")
        print(f"     Decrypted Fares: {cluster['fares']} → Signature: {cluster['signature']}")
        print(f"     Original Fares: {cluster['original_fares']}")
        print(f"     Timestamp: {cluster['first_timestamp']}")
        
        # Verify the fare pattern
        A, B, C = cluster['fares']
        expected_B = abs(A - C) + (A % C)
        print(f"     Verification: |{A}-{C}| + ({A} mod {C}) = {abs(A-C)} + {A%C} = {expected_B} ✓")
    
    # Location verification
    print("\n🗺️  Verify location at:")
    print(f"   Google Maps: https://www.google.com/maps?q={lat},{lon}")
    print(f"   OpenStreetMap: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=18")
    
    print("\n📍 This location is in Algeria (Constantine region)")
    print("=" * 80)

if __name__ == "__main__":
    main()


