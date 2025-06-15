# **Your Personal Agent at Work**
### **📌 Project Description**
Personal Agent is a fully interactive, AI-powered assistant that answers questions about an individual by intelligently synthesizing data from their GitHub, LinkedIn, Medium, and resume. Built using **LangChain, LangGraph, Agno, Supabase and Streamlit**, this app enables users to gain holistic insights into a person's professional and personal background in a conversational format.

**The app is designed to:**

Extract and summarize structured and unstructured data from different platforms.

Respond to natural language queries using LLMs (like GPT-4o).

Dynamically update context, remember previous chats, and send responses via email.

Securely handle API keys and authentication using Supabase.

### **🌟 Unique Selling Points (USP)**
**Multi-source understanding:** Integrates GitHub, LinkedIn, Medium articles, and resume data.

**Conversational flow:** Uses memory and history for more relevant, flowing conversations.

**Fully user-controlled:** Users input their own API keys and profile URLs—no data is stored permanently.

**Email-ready:** Users can receive their responses via email with a single checkbox.

**Secure authentication:** Signup/Login system using Supabase ensures access control.

### **🚀 How to Use the App**
Go to the deployed app: [Streamlit App Link](https://personalagent-6bxcakdbfhwqtfredwh36w.streamlit.app/)

Login or Sign Up using your email credentials.

Enter API Keys in the sidebar:

OpenAI (for answering questions)

Firecrawl (for Medium article scraping)

Proxycurl (for LinkedIn profile extraction)

Provide your profile URLs:

GitHub (user or repo)

LinkedIn profile URL

Medium article URLs (comma-separated)

(Optional) Upload your resume (PDF format).

**Ask any question like:**

"What are Dhruv’s top skills?"

"Tell me about Dhruv’s recent GitHub activity."

"Summarize Dhruv’s Medium posts."

Optionally check "Email me this response" and input your email to receive the output in your inbox.

## **🛠 Tech Stack**

| Category                 | Tools / Libraries                                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------------- |
| **Frontend**             | [Streamlit](https://streamlit.io/) – For building and deploying the UI                             |
| **LLM & AI Agents**      | [LangChain](https://www.langchain.com/), [LangGraph](https://www.langgraph.ai/)                    |
| **LLM API**              | [OpenAI GPT-4o](https://platform.openai.com/docs/models/gpt-4o)                                    |
| **Authentication**       | [Supabase Auth](https://supabase.com/docs/guides/auth)                                             |
| **Database**             | [Supabase Postgres DB](https://supabase.com/docs/guides/database) – For chat logs                  |
| **Web Scraping APIs**    | [Proxycurl](https://nubela.co/proxycurl) – LinkedIn<br>[Firecrawl](https://firecrawl.dev) – Medium |
| **PDF Parsing**          | [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) – For extracting resume text                  |
| **Email Sending**        | [SMTP + smtplib](https://docs.python.org/3/library/smtplib.html)                                   |
| **Environment Handling** | `python-dotenv`, `st.secrets` in Streamlit                                                         |
| **Package Management**   | `requirements.txt`, `uv` (used by Streamlit Cloud)                                                 |


## **🧠 Project Architecture**

The Personal Agent system follows a modular and sequential architecture, designed to process a user’s natural language query and generate a context-rich, intelligent response by leveraging multiple data sources. Here's how it works:

**🔁 1. User Input (Natural Language Query)**
The user enters a question into the chat interface (built using Streamlit).

Example: "What are Dhruv's main projects?"

**🧩 2. LangGraph Execution Flow Begins**
The query is passed through a LangGraph workflow, where each node represents a module (agent) responsible for processing a specific data source.

**🔗 3. Parallel Data Agents (Executed Sequentially)**
Each of the following agents extracts insights from its respective platform:

📦 GitHub Agent
Uses the LangChain GitHub Toolkit (via Agno).

Fetches repository info, stars, languages, branches, and issues for the provided GitHub profile or repo.

📰 Medium Agent
Uses the Firecrawl API to scrape Medium articles.

Performs LLM-based summarization relevant to the user’s query.

👔 LinkedIn Agent
Uses the Proxycurl API to retrieve structured data from the LinkedIn profile.

Summarized using OpenAI's GPT-4o for relevance to the query.

**🧠 4. Final Aggregation Node**
Combines all agent responses along with any uploaded resume (PDF) content.

Constructs a context-rich prompt including:

GitHub Info

Medium Summary

LinkedIn Summary

Resume Details (if uploaded)

Previous conversation history (for memory)

The final response is generated by OpenAI’s GPT-4o model.

**💾 5. Chat History Storage**
Both the query and the LLM-generated response are stored in a Supabase PostgreSQL database along with the user’s email.

**📧 6. Optional Email Response**
If enabled, the system uses a configured SMTP agent to email the response to the user’s provided email address.
Here's a visual and textual breakdown of how the Personal Agent system works.

![image](https://github.com/user-attachments/assets/08f68445-b263-45a9-bcca-fcd6e3100f9c)
