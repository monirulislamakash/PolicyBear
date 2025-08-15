import requests
import time
import requests
import json

#Get countyfips From ZIP Code

def get_lat_lon_and_state(zip_code):
    """Fetch latitude, longitude, and state abbreviation for a given ZIP code."""
    url = f"http://api.zippopotam.us/us/{zip_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        place = data['places'][0]
        return float(place['latitude']), float(place['longitude']), place['state abbreviation']
    except requests.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None, None, None

def get_county_fips_with_state(zip_code):
    """Get county FIPS code and state abbreviation for a given ZIP code."""
    lat, lon, state_abbr = get_lat_lon_and_state(zip_code)
    if lat is None or lon is None:
        return None, None
    
    url = f"https://geo.fcc.gov/api/census/block/find?format=json&latitude={lat}&longitude={lon}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        county_fips = data['County']['FIPS']
        return county_fips, state_abbr
    except requests.RequestException as e:
        print(f"Error fetching FIPS code: {e}")
        return None, state_abbr

# API Intgration

API_KEY = "aG9hPbCc87sjREuz539FtF3QJn1Ieq4a"
URL = f"https://marketplace.api.healthcare.gov/api/v1/plans/search?apikey={API_KEY}"

def get_Offer_details(get_Zip,county_fips,state_abbr,get_income,get_age,get_gender):
    payload = {
    "household": {
        "income": get_income,
        "people": [
            {
                "age":get_age,
                "aptc_eligible": True,
                "gender": get_gender,
                "uses_tobacco": False
            }
        ]
    },
    "market": "Individual",
    "place": {
        "countyfips": county_fips,
        "state": state_abbr,
        "zipcode": get_Zip,
    },
    "year": 2025
    }

    headers = {"Content-Type": "application/json"}
    output_filename = "filtered_healthcare_plans.json"
    response = requests.post(URL, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        
        # Filter only required fields
        filtered_plans = []
        for plan in response_data.get("plans", []):
            issuer_name = plan.get("issuer", {}).get("name", "N/A")
            deductibles = plan.get("deductibles", [])[0].get("amount", "N/A")
            filtered_plans.append({
                "id": plan.get("id"),
                "name": plan.get("name"),
                "premium": plan.get("premium"),
                "premium_w_credit": plan.get("premium_w_credit"),
                "ehb_premium": plan.get("ehb_premium"),
                "pediatric_ehb_premium": plan.get("pediatric_ehb_premium"),
                "aptc_eligible_premium": plan.get("aptc_eligible_premium"),
                "metal_level": plan.get("metal_level"),
                "state":plan.get("state"),
                "issuer_name":issuer_name,
                "deductibles":deductibles
            })
        
        # Save filtered response
        # with open(output_filename, 'w') as f:
        #     json.dump(filtered_plans, f, indent=4)
        return filtered_plans
        
        print(f"Filtered plans saved to '{output_filename}'")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

