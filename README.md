# 🚀 Taxi Hotspot Hunt - Solution

## Challenge Overview
Finding a hidden hotspot in Yassir taxi trip data by detecting valid clusters of 3 trips that follow a specific fare pattern.

## Solution Approach

### Step 1: Data Cleaning
- **Initial dataset**: 527 rows (with intentional distortions)
- **After removing rows with empty values**: 259 valid rows
- This significantly reduced the search space and removed decoy data

### Step 2: Fare Decryption
The challenge mentioned that "fares aren't the real ones" and were "shifted using a specific key."

After testing various decryption keys (0 to 7000), we found:
- **Decryption Key**: 3200
- Decrypted fare = Original fare - 3200

### Step 3: Cluster Detection
A valid cluster must satisfy:

1. **Different taxis**: All 3 trips have distinct car IDs
2. **Fare pattern**: Middle fare B follows: `B = |A - C| + (A mod C)`
   - Where A = first fare, B = middle fare, C = third fare
3. **Chronological order**: Trips sorted by timestamp
4. **Same location**: All 3 trips at the same coordinates

### Step 4: Scoring & Tie-Breaking
- Cluster signature = Sum of 3 fares
- Location score = Sum of all cluster signatures at that location
- Tie-breaking rules:
  1. Highest total score
  2. Earliest valid cluster
  3. Largest latitude
  4. Largest longitude

## Results

### 🎯 Hotspot Found
- **Coordinates**: (35.590001, 6.160020)
- **Location**: Constantine, Algeria
- **DMS Format**: 35°35'24.0"N 6°09'36.1"E

### 📊 Statistics
- **Total Valid Clusters**: 1
- **Total Score**: 3,451
- **Earliest Cluster**: 2025-01-01 08:10:00

### 🚕 Cluster Details
- **Taxi IDs**: TX48, TX08, TX33
- **Decrypted Fares**: (817, 1317, 1317)
- **Original Fares**: (4017, 4517, 4517)
- **Signature**: 3,451

### ✅ Fare Pattern Verification
```
A = 817, B = 1317, C = 1317
Expected B = |817 - 1317| + (817 mod 1317)
           = 500 + 817
           = 1317 ✓
```

## Key Insights

1. **Data Quality Matters**: Removing incomplete rows (from 527 to 259) was crucial to eliminate decoys
2. **Systematic Key Testing**: Tested decryption keys from 0-7000 to find the correct shift (3200)
3. **Geographic Filtering**: Limited search to Algeria coordinates (18-38°N, -9-12°E)
4. **Pattern Validation**: The modulo-based fare formula was the key to identifying authentic clusters

## Technology Stack
- Python 3.x
- pandas (data manipulation)
- openpyxl (Excel file handling)

## How to Run
```bash
python "# find_taxi_hotspot.py"
```

## Verification
Verify the location on:
- [Google Maps](https://www.google.com/maps?q=35.590001,6.16002)
- [OpenStreetMap](https://www.openstreetmap.org/?mlat=35.590001&mlon=6.16002&zoom=18)

---
**Challenge**: Yassir Taxi Hotspot Hunt  
**Status**: ✅ Solved  
**Location**: Constantine, Algeria
