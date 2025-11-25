import requests

def get_uk_carbon_intensity(postcode: str = "national") -> dict:
    """Get live UK grid carbon intensity in gCO2/kWh.
    
    Args:
        postcode: UK postcode (e.g., 'G1') or 'national' for UK average
    
    Returns:
        Dictionary with region and gCO2_per_kWh
    """
    try:
        if postcode.lower() == "national":
            url = "https://api.carbon-intensity.org.uk/intensity"
        else:
            url = f"https://api.carbon-intensity.org.uk/regional/postcode/{postcode}"
        
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if postcode.lower() == "national":
            intensity = data["data"][0]["intensity"]["actual"]
            return {"region": "National", "gCO2_per_kWh": intensity}
        else:
            intensity = data["data"][0]["data"][0]["intensity"]["forecast"]
            region_name = data["data"][0]["shortname"]
            return {"region": region_name, "gCO2_per_kWh": intensity}
    except:
        return {"region": postcode, "gCO2_per_kWh": 141, "note": "Using 2025 UK average"}
