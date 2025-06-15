
# from agno.agent import Agent
# from agno.tools.github import GithubTools

# def query_github_agent(query: str, github_profile: str):
#     # Create the GitHub tools with safe read-only access
#     github_tools = GithubTools(
#         search_repositories=True,      # Search for repositories
#         get_repository=True,           # Get repository details
#         get_repository_languages=True, # Get repository languages
#         get_repository_stars=True,     # Get repository stars
#         list_branches=True,            # List repository branches
#         get_repository_with_stats=True, # Get repository with statistics
#         list_issues=True,              # List issues (read-only)
#         get_issue=True,                # Get specific issue details
#         get_pull_requests=True,        # Get pull requests
#         get_pull_request=True,         # Get specific pull request
#         # Explicitly disable write operations for safety
#         create_issue=False,
#         create_repository=False,
#         delete_repository=False,
#         create_file=False,
#         update_file=False,
#         delete_file=False,  
#     )

#     # Create the agent
#     github_agent = Agent(
#         instructions=[
#             f"Use your tools to fetch data about the GitHub user or repository: '{github_profile}'",
#             "Only retrieve factual data. Do not generate or summarize content.",
#             "You have read-only access.",
#             ""
#         ],
#         tools=[github_tools],
#         show_tool_calls=True,
#     )

#     # Run the query
#     try:
#         return github_agent.run(query)
#     except Exception as e:
#         return f"Error: {str(e)}"



from agno.agent import Agent
from agno.tools.github import GithubTools
import os

def query_github_agent(query: str, github_profile: str, openai_api_key: str):
    """
    Query GitHub agent with user-provided OpenAI API key
    
    Args:
        query: The user's question
        github_profile: GitHub username or repository
        openai_api_key: User's OpenAI API key from Streamlit input
    """
    
    # Store original environment variable if it exists
    original_openai_key = os.environ.get('OPENAI_API_KEY')
    
    try:
        # Temporarily set the user's API key in environment for agno to use
        os.environ['OPENAI_API_KEY'] = openai_api_key
            
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
        
        # Create the agent with improved instructions
        github_agent = Agent(
            instructions=[
                f"Use your tools to fetch data about the GitHub user or repository: '{github_profile}'",
                "Analyze the user's query and determine what specific information they're looking for.",
                "If they're asking about projects, focus on repositories and their details.",
                "If they're asking about coding activity, look at commit history and contributions.",
                "If they're asking about skills, analyze the programming languages used across repositories.",
                "Only retrieve factual data. Do not generate or summarize content unnecessarily.",
                "Provide comprehensive information relevant to the user's specific question.",
                "You have read-only access for safety.",
            ],
            tools=[github_tools],
            show_tool_calls=True,
        )
        
        # Run the query
        response = github_agent.run(query)
        return response
        
    except Exception as e:
        error_msg = f"GitHub Agent Error: {str(e)}"
        print(error_msg)  # For debugging
        return error_msg
        
    finally:
        # Restore original environment variable
        if original_openai_key is not None:
            os.environ['OPENAI_API_KEY'] = original_openai_key
        else:
            # Remove the key if it wasn't there originally
            os.environ.pop('OPENAI_API_KEY', None)
