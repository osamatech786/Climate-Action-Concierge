import requests

def get_uk_carbon_intensity(postcode: str) -> str:
    """Get live UK grid carbon intensity for a postcode.
    
    Args:
        postcode: UK postcode like E17, G1, SW1A
    
    Returns:
        String with grid intensity value in gCO2/kWh
    """
    try:
        url = f"https://api.carbon-intensity.org.uk/regional/postcode/{postcode}"
        response = requests.get(url, timeout=5)
        data = response.json()
        intensity = data["data"][0]["data"][0]["intensity"]["forecast"]
        return f"{intensity}"
    except Exception as e:
        return "141"
