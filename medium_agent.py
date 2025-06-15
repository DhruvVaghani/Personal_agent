# Medium Agent

import requests
from langchain.chat_models import ChatOpenAI

# MEDIUM_POST_URLS = [
#     "https://medium.com/@dhruvvaghani5356/hey-im-dhruv-let-s-dive-into-data-ai-and-real-world-impact-206069edd468"
# ]

# 🔥 Function to fetch content using Firecrawl (takes firecrawl_api_key as argument)
def fetch_selected_medium_posts(medium_urls: list[str], firecrawl_api_key: str) -> str:
    all_content = ""
    for url in medium_urls:
        try:
            response = requests.post(
                "https://api.firecrawl.dev/v1/scrape",
                headers={"Authorization": f"Bearer {firecrawl_api_key}"},
                json={"url": url}
            )
            data = response.json()
            content = data.get("content", "")
            all_content += f"\n\n---\nPost URL: {url}\n{content}\n"
        except Exception as e:
            all_content += f"\n\n[Error fetching {url}]: {e}\n"
    return all_content

# 🧠 Function to summarize using OpenAI (takes openai_api_key as argument)
def generate_llm_summary(scraped_content: str, query: str, openai_api_key: str) -> str:
    llm = ChatOpenAI(model="gpt-4o", api_key=openai_api_key)
    prompt = (
        f"Use the following Medium post content to answer the user's query:\n\n"
        f"{scraped_content}\n\n"
        f"Question: {query}\n"
        f"Answer in a concise, natural tone:"
    )
    return llm.invoke(prompt).content
