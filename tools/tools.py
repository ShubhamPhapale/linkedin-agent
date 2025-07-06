from langchain_community.tools import TavilySearchResults

def get_profile_url_tavily(name_and_info: str):
    Search = TavilySearchResults()
    res = Search.run(f"{name_and_info}")

    return res[0]["url"] # res