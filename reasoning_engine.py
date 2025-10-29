import os


def get_reasoned_answer(api_key: str, user_query: str, notion_data: str, git_data: str) -> str:
    """
    Attempts to use OpenAI to analyze Notion and Git data and provide a coherent answer.

    Falls back to a local summary if the OpenAI client isn't available or a network/connection
    error occurs so the script remains usable for offline testing.
    """

    print("🧠 Preparing reasoning step (OpenAI)")

    try:
        from openai import OpenAI
    except Exception:
        # openai package not available — return a safe fallback
        return (
            "⚠️ OpenAI client not available.\n"
            "Summary fallback:\n"
            f"User Query: {user_query}\n\n"
            "Notion Data:\n" + (notion_data or "(no notion data)") + "\n\n"
            "Git Data:\n" + (git_data or "(no git data)") + "\n\n"
            "(Install the openai package and set OPENAI_API_KEY to enable real reasoning.)"
        )

    try:
        if not api_key:
            return (
                "⚠️ OPENAI_API_KEY is not set.\n"
                "Summary fallback:\n"
                f"User Query: {user_query}\n\n"
                "Notion Data:\n" + (notion_data or "(no notion data)") + "\n\n"
                "Git Data:\n" + (git_data or "(no git data)") + "\n\n"
                "(Set OPENAI_API_KEY to enable real reasoning.)"
            )

        print("🧠 Sending data to OpenAI for contextual reasoning...")
        client = OpenAI(api_key=api_key)

        system_prompt = (
            "You are an intelligent internal assistant for a development team. "
            "Your goal is to bridge documentation (Notion) and code (Git). "
            "Analyze the retrieved information from both sources to answer the user's question. "
            "You MUST provide attribution by citing which Notion pages and which Git files were used."
        )

        user_prompt = f"""
User's Question: "{user_query}"

---
DATA RETRIEVED FROM NOTION:
{notion_data}
---
DATA RETRIEVED FROM GIT REPOSITORY:
{git_data}
---

Please provide a concise, professional, and human-readable answer that directly addresses the User's Question based ONLY on the data provided above.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        # Try to detect common connection/network errors and return a friendly fallback
        msg = str(e)

        # Prefer to test for requests exceptions if requests is available
        is_conn_error = False
        try:
            import requests as _requests
            if isinstance(e, _requests.exceptions.RequestException):
                is_conn_error = True
        except Exception:
            # requests not available or other import issue; fall back to message checks
            pass

        # Generic checks for connection-related messages
        if (is_conn_error
                or 'connection' in msg.lower()
                or 'failed to establish' in msg.lower()
                or 'connection aborted' in msg.lower()
                or 'timeout' in msg.lower()):
            return (
                "⚠️ OpenAI connection failed (network issue).\n"
                "Summary fallback:\n"
                f"User Query: {user_query}\n\n"
                "Notion Data:\n" + (notion_data or "(no notion data)") + "\n\n"
                "Git Data:\n" + (git_data or "(no git data)") + "\n\n"
                "(Check OPENAI_API_KEY, network access, or set OPENAI_API_KEY empty to use local fallback.)"
            )

        # Unknown error — return the original message
        return f"❌ OpenAI Reasoning Error: {e}"