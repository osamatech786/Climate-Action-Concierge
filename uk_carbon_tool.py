import requests

def get_uk_carbon_intensity(region: str = "national") -> dict:
    """Fetch live UK grid carbon intensity in gCO2/kWh.
    
    Args:
        region: Either 'national' or UK postcode (e.g., 'SW1A1AA')
    
    Returns:
        Dictionary with region name and gCO2_per_kWh value
    """
    try:
        if region.lower() == "national":
            url = "https://api.carbon-intensity.org.uk/intensity"
        else:
            url = f"https://api.carbon-intensity.org.uk/regional/postcode/{region}"
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if region.lower() == "national":
            intensity = data["data"][0]["intensity"]["actual"]
            return {"region": "National", "gCO2_per_kWh": intensity}
        else:
            intensity = data["data"][0]["data"][0]["intensity"]["forecast"]
            region_name = data["data"][0]["shortname"]
            return {"region": region_name, "gCO2_per_kWh": intensity}
    except Exception as e:
        error_msg = f"Using UK average (API error: {str(e)})"
        return {"region": region, "gCO2_per_kWh": 233, "note": error_msg}
