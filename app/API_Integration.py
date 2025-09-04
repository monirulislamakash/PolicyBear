import requests
import time
import json
import logging

# Set up logging for better visibility of what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Helper Functions (remain the same) ---

def robust_get(url, retries=3, delay=2):
    """
    A robust wrapper for requests.get with retries and delays.
    It returns the response object or None on failure.
    """
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.warning(f"Request to {url} failed (attempt {i+1}/{retries}): {e}")
            if i < retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error(f"All retry attempts failed for {url}.")
                return None

def get_lat_lon_and_state(zip_code):
    """Fetch latitude, longitude, and state abbreviation for a given ZIP code."""
    url = f"http://api.zippopotam.us/us/{zip_code}"
    response = robust_get(url)
    if response is None:
        return None, None, None
    
    try:
        data = response.json()
        place = data['places'][0]
        return float(place['latitude']), float(place['longitude']), place['state abbreviation']
    except (IndexError, KeyError) as e:
        logging.error(f"Error parsing zippopotam.us response: {e}")
        return None, None, None

# --- Main Function with API Fallback ---

def get_county_fips_with_state(zip_code):
    """
    Gets county FIPS code and state abbreviation using a list of fallback APIs.
    It tries each API in order until a successful response is received.
    """
    lat, lon, state_abbr = get_lat_lon_and_state(zip_code)
    if lat is None or lon is None:
        return None, None

    # Define a list of fallback API functions
    # Each function should take lat, lon, and state_abbr and return a (fips, state_abbr) tuple
    api_providers = [
        # get_fips_from_fcc_api,
        get_fips_from_census_api
    ]

    for provider_function in api_providers:
        fips, state = provider_function(lat, lon, state_abbr)
        if fips:
            # If the provider function returns a valid FIPS code, we're done
            logging.info(f"Successfully retrieved FIPS from {provider_function.__name__}")
            return fips, state
        else:
            logging.warning(f"{provider_function.__name__} failed. Trying the next provider.")

    logging.error("All FIPS code providers failed.")
    return None, state_abbr

# --- Provider Functions (one for each API) ---

# def get_fips_from_fcc_api(lat, lon, state_abbr):
#     """
#     Retrieves FIPS from the original FCC Geo API.
#     Returns (fips, state_abbr) or (None, state_abbr) on failure.
#     """
#     logging.info("Attempting to use FCC Geo API...")
#     url = f"https://geo.fcc.gov/api/census/block/find?format=json&latitude={lat}&longitude={lon}"
#     response = robust_get(url)
#     if response is None:
#         return None, state_abbr

#     try:
#         data = response.json()
#         county_fips = data['County']['FIPS']
#         return county_fips, state_abbr
#     except (KeyError, IndexError) as e:
#         logging.error(f"Error parsing FCC Geo API response: {e}")
#         return None, state_abbr

def get_fips_from_census_api(lat, lon, state_abbr):
    """
    Retrieves FIPS from the U.S. Census Bureau Geocoder API.
    Returns (fips, state_abbr) or (None, state_abbr) on failure.
    """
    logging.info("Attempting to use U.S. Census Bureau Geocoder API...")
    url = f"https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={lon}&y={lat}&benchmark=Public_AR_Current&vintage=Census2020_Current&format=json"
    response = robust_get(url)
    if response is None:
        return None, state_abbr

    try:
        data = response.json()
        if not data['result']['geographies']['Counties']:
            logging.warning("No county information found from Census API.")
            return None, state_abbr
            
        county_data = data['result']['geographies']['Counties'][0]
        county_fips = county_data['GEOID']
        return county_fips, state_abbr
    except (KeyError, IndexError) as e:
        logging.error(f"Error parsing U.S. Census Geocoder response: {e}")
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
                "plan":f'{issuer_name.split()[0]} {plan.get("metal_level")} Plan',
                # "premium": plan.get("premium"),
                "premium": plan.get("ehb_premium"),
                "subsidy ": plan.get("premium_w_credit"),
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
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

