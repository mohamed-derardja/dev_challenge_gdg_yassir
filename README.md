# Taxi Hotspot Hunt - Solution

## Challenge Overview
Finding a hidden hotspot in Yassir taxi trip data by detecting valid clusters of 3 trips that follow a specific fare pattern.

## Solution Approach

### Step 1: Data Cleaning
- **Initial dataset**: 526 rows (with intentional distortions)
- **After removing rows with empty values**: 259 valid rows
- This significantly reduced the search space and removed decoy data

### Step 2: Fare Decryption
The challenge mentioned that "fares aren't the real ones" and were "shifted using a specific key."
After testing various decryption keys (0 to 7000), we found:
- **Decryption Key**: 2017 (Yassir founding year)
- **Formula**: Decrypted fare = Original fare - 2017

### Step 3: Cluster Detection
A valid cluster must satisfy:

1. **Different taxis**: All 3 trips have distinct car IDs
2. **Fare pattern**: Middle fare B follows: B = |A - C| + (A mod C)
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

### Hotspot Found
- **Coordinates**: (35.6339001, 6.2709666)
- **Total Score**: 7000.0
- **Earliest Cluster**: 2025-01-01 11:00:00

## Key Improvements (Updated)
-  Fixed file path handling with try-except block
-  Code now runs without errors
-  Successfully identifies hotspots with robust error handling
-  Works with multiple file path configurations

## Technology Stack
- Python 3.x
- pandas (data manipulation)
- collections.defaultdict (efficient grouping)

## How to Run
\\\ash
python find_taxi_hotspot.py
\\\

## Verification
Verify the location on:
- [Google Maps](https://www.google.com/maps?q=35.6339001,6.2709666)
- [OpenStreetMap](https://www.openstreetmap.org/?mlat=35.6339001&mlon=6.2709666&zoom=18)

---
**Challenge**: Yassir Taxi Hotspot Hunt
**Status**:  Solved & Optimized
**Location**: (35.6339001, 6.2709666)
**Solution Author**: Mihiderar
