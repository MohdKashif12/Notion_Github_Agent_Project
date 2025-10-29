import requests
import os

GITHUB_API_URL = "https://api.github.com"


def search_git_repo(api_key: str, repo_owner: str, repo_name: str, query_text: str) -> str:
    """Searches a specific GitHub repo for code containing the query text."""

    if not api_key:
        return "❌ Git: Missing API key for GitHub."

    # We use GitHub's code search API
    search_query = f"{query_text}+repo:{repo_owner}/{repo_name}"
    search_url = f"{GITHUB_API_URL}/search/code?q={search_query}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.github.v3+json",
    }

    print(f"🤖 Searching Git repo {repo_name} for code: '{query_text}'...")

    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()

        results = response.json().get("items", [])

        if not results:
            return "❌ Git: No matching code files found in the repository."

        file_paths = []
        for item in results[:5]:  # Limit to top 5 results
            path = item.get("path", "No Path")
            url = item.get("html_url", "No URL")
            file_paths.append(f"File: {path}, URL: {url}")

        return "\n".join(file_paths)

    except requests.exceptions.RequestException as e:
        return f"❌ Git Connection Error: {e}"