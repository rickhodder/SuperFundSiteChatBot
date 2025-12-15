"""Find policy addresses that are > 50 miles from any SuperFund site."""
import pandas as pd
from geopy.distance import geodesic

# Load data
policies = pd.read_csv('data/raw/policies.csv', dtype={'PostalCode': str})
sites = pd.read_csv('data/raw/superfund_sites.csv', dtype={'PostalCode': str})

print('Checking policies for distance to nearest SuperFund site...\n')

safe_policies = []

for idx, policy in policies.iterrows():
    policy_loc = (policy['Latitude'], policy['Longitude'])
    
    # Find minimum distance to any site
    min_dist = float('inf')
    for _, site in sites.iterrows():
        site_loc = (site['Latitude'], site['Longitude'])
        dist = geodesic(policy_loc, site_loc).miles
        min_dist = min(min_dist, dist)
    
    # If more than 50 miles away, it's safe
    if min_dist > 50:
        safe_policies.append({
            'address': f"{policy['Address']}, {policy['City']}, {policy['State']} {policy['PostalCode']}",
            'policy_number': policy['PolicyNumber'],
            'distance': min_dist
        })

# Print results
if safe_policies:
    print(f"Found {len(safe_policies)} SAFE policies (> 50 miles from any site):\n")
    for p in safe_policies[:5]:  # Show first 5
        print(f"✅ {p['address']}")
        print(f"   Policy: {p['policy_number']}")
        print(f"   Nearest site: {p['distance']:.1f} miles away\n")
else:
    print("❌ No policies found that are more than 50 miles from all sites.")
