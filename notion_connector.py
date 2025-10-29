import requests
import os

# Base URL and Version for Notion API
NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def search_notion(api_key: str, query_text: str) -> str:
    """Fetches Notion pages relevant to the query."""
    search_url = f"{NOTION_API_URL}/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }
    payload = {"query": query_text}

    print(f"🤖 Searching Notion for docs: '{query_text}'...")

    try:
        response = requests.post(search_url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()  # Check for bad status codes

        results = response.json().get("results", [])

        if not results:
            return "❌ Notion: No matching documentation pages found."

        page_summaries = []
        for page in results[:5]:  # Limit to top 5 results
            # Extract Title and URL from the Notion page object
            # Note: Notion page object structure is complex. This is a simplified fetch.
            title_property = page.get("properties", {}).get("title", {}).get("title", [{}])
            title = title_property[0].get("plain_text", "No Title Available") if title_property else "No Title Available"
            url = page.get("url", "No URL")

            page_summaries.append(f"Title: {title}, URL: {url}")

        return "\n".join(page_summaries)

    except requests.exceptions.RequestException as e:
        return f"❌ Notion Connection Error: {e}"