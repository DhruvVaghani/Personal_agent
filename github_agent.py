
from agno.agent import Agent
from agno.tools.github import GithubTools

def query_github_agent(query: str, github_profile: str):
    # Create the GitHub tools with safe read-only access
    github_tools = GithubTools(
        search_repositories=True,      # Search for repositories
        get_repository=True,           # Get repository details
        get_repository_languages=True, # Get repository languages
        get_repository_stars=True,     # Get repository stars
        list_branches=True,            # List repository branches
        get_repository_with_stats=True, # Get repository with statistics
        list_issues=True,              # List issues (read-only)
        get_issue=True,                # Get specific issue details
        get_pull_requests=True,        # Get pull requests
        get_pull_request=True,         # Get specific pull request
        # Explicitly disable write operations for safety
        create_issue=False,
        create_repository=False,
        delete_repository=False,
        create_file=False,
        update_file=False,
        delete_file=False,  
    )

    # Create the agent
    github_agent = Agent(
        instructions=[
            f"Use your tools to fetch data about the GitHub user or repository: '{github_profile}'",
            "Only retrieve factual data. Do not generate or summarize content.",
            "You have read-only access.",
            ""
        ],
        tools=[github_tools],
        show_tool_calls=True,
    )

    # Run the query
    try:
        return github_agent.run(query)
    except Exception as e:
        return f"Error: {str(e)}"
