from vault import get_secret
import requests

def search(query):
    """Search the web using SerpAPI and return top result."""
    api_key = get_secret("SERPAPI_KEY")
    params = {
        "q": query,
        "api_key": api_key,
        "num": 3
    }
    url = "https://serpapi.com/search"
    try:
        response = requests.get(url, params=params)
        data = response.json()

        results = data.get("organic_results", [])
        if not results:
            return "No results found."

        reply = []
        for i, r in enumerate(results):
            title = r.get("title")
            link = r.get("link")
            snippet = r.get("snippet", "")
            reply.append(f"{i+1}. 🔗 {title}\n{snippet}\n{link}\n")
        return "\n".join(reply)

    except Exception as e:
        return f"Error: {e}" 