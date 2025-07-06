import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/ShubhamPhapale/4800e576b421e3d7e813a04cd20dc1e5/raw/869bb7ce2278b452ac200ea8cca894418a2bc5f1/shubhamphapale-srapin.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey" : os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl" : linkedin_profile_url
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10
        )

    data = response.json().get("person")
    # data = {
    #     k : v
    #     for k, v in data.items()
    #     if v not in ([], "", "", None) and k not in ["certifications"]
    # }

    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/bharatiphapale/",
            mock=True
        )
    )