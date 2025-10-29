import os
from dotenv import load_dotenv

# Import the functions from your connector files
from notion_connector import search_notion
from git_connector import search_git_repo
from reasoning_engine import get_reasoned_answer

def run_agent_flow(user_query: str, search_term: str):
    """
    Executes the agent's core flow: Authentication, Retrieval, and Reasoning.
    """
    # 1. Load Environment Variables (API Keys)
    load_dotenv()
    
    # Load and normalize environment variables (strip stray whitespace/newlines)
    NOTION_KEY = (os.getenv("NOTION_API_KEY") or "").strip()
    GIT_KEY = (os.getenv("GIT_API_KEY") or "").strip()
    OPENAI_KEY = (os.getenv("OPENAI_API_KEY") or "").strip()
    REPO_OWNER = (os.getenv("GIT_REPO_OWNER") or "").strip()
    REPO_NAME = (os.getenv("GIT_REPO_NAME") or "").strip()
    
    if not all([NOTION_KEY, GIT_KEY, OPENAI_KEY, REPO_OWNER, REPO_NAME]):
        print("❌ Error: One or more API keys or repository details are missing in the .env file. Please check and try again.")
        return

    print("\n--- AGENT STARTING CONTEXTUAL SEARCH ---")
    print(f"User Query: {user_query}")
    print(f"Internal Search Term: {search_term}")
    print("------------------------------------------")

    # 2. Retrieval Step 1: Notion Connector
    notion_results = search_notion(NOTION_KEY, search_term)
    
    # 3. Retrieval Step 2: Git Connector
    git_results = search_git_repo(GIT_KEY, REPO_OWNER, REPO_NAME, search_term)
    
    # 4. Reasoning Step: OpenAI
    final_answer = get_reasoned_answer(OPENAI_KEY, user_query, notion_results, git_results)
    
    # 5. Output Format (As required by PDF)
    print("\n========================================================")
    print("             ✅ FINAL AGENT RESPONSE ✅")
    print("========================================================")
    print(final_answer)
    print("========================================================\n")


# === EXECUTION: RUNNING THE EXAMPLE SCENARIOS ===

def main():
    # Quick visible startup message to help debugging silent runs
    print(">>> main_agent.py starting...")

    # Scenario A: Find implementation details for a task.
    # This is the primary scenario required by the PDF.
    scenario_a_query = "What tasks in Notion relate to the payment service, and where is that logic implemented in Git?"
    search_term_a = "payment service"
    run_agent_flow(scenario_a_query, search_term_a)

    # Scenario B: Project Traceability (uncomment to run second)
    # scenario_b_query = "Summarize the 'User Authentication Flow' Notion page and find the relevant files in the Git repo that mention 'JWT' or 'session'."
    # search_term_b = "User Authentication Flow JWT session"
    # run_agent_flow(scenario_b_query, search_term_b)


if __name__ == "__main__":
    import traceback, sys
    try:
        main()
    except Exception as exc:
        # Ensure any unexpected exception is visible
        print("❌ Unhandled exception while running main_agent.py:")
        traceback.print_exc()
        # exit with non-zero so CI or shell can detect failure
        sys.exit(1)