
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict
import fitz  # PyMuPDF

from github_agent import query_github_agent
from medium_agent import fetch_selected_medium_posts, generate_llm_summary
from linkedin_agent import generate_linkedin_summary
from email_agent import send_email
import webbrowser
import streamlit as st
st.set_page_config(page_title="Personal Agent - Ask About Dhruv", layout="centered")



from dotenv import load_dotenv
load_dotenv()
from supabase import create_client
import os
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
github_token = st.secrets["GITHUB_ACCESS_TOKEN"]
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



# Session state to track login
if "user" not in st.session_state:
    st.session_state.user = None

# ✅ Show login/signup UI only if not logged in
if not st.session_state.user:
    st.title("🔐 Login to Use Personal Agent")

    auth_mode = st.radio("Choose action", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button(auth_mode):
        if auth_mode == "Login":
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if response.user:
                st.session_state.user = response.user
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Login failed. Check your credentials.")
        else:  # Sign Up
            response = supabase.auth.sign_up({"email": email, "password": password})
            if response.user:
                st.success("Signed up successfully! You can now log in.")
            else:
                st.error("Signup failed. Email might already be registered.")
        
    
    st.stop()  # Stop the app here if not logged in

if st.session_state.user:
            st.sidebar.success(f"Logged in as: {st.session_state.user.email}")
            if st.sidebar.button("🔓 Log out"):
                st.session_state.user = None
                st.rerun()



st.sidebar.title("🔐 API Keys")

st.session_state.openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
st.session_state.firecrawl_api_key = st.sidebar.text_input("Firecrawl API Key", type="password")
st.session_state.proxycurl_api_key = st.sidebar.text_input("Proxycurl API Key", type="password")
with st.sidebar:
    st.markdown("----")
    st.markdown("👨‍💻 Built by **Dhruv Vaghani**")
    st.markdown("[GitHub](https://github.com/dhruvvaghani) | [LinkedIn](https://linkedin.com/in/dhruv-vaghani)")



with st.expander("🔗 Enter Profile URLs (GitHub, LinkedIn, Medium)",expanded = True):
    # User inputs for profile URLs
    st.session_state.github_profile = st.text_input("GitHub Profile or Repo")
    st.session_state.linkedin_profile = st.text_input("LinkedIn Profile URL")
    st.session_state.medium_urls = st.text_area("Medium Article URLs (comma-separated, optional)")
if not all([
    st.session_state.openai_api_key,
    st.session_state.firecrawl_api_key,
    st.session_state.proxycurl_api_key,
    st.session_state.github_profile,
    st.session_state.linkedin_profile
]):
    # Main page instructions
    st.markdown("""
    ### 🚀 Getting Started
    To use this Personal Agent app, you'll need API keys for the services listed below.

    **🔑 Required Keys:**
    - OpenAI (for answering questions)
    - Firecrawl (to scrape Medium posts)
    - Proxycurl (to summarize LinkedIn profiles)

    👉 Follow the instructions given below to generate your API keys.

    💡 Example questions:
    - "What sport is Dhruv interested in?"
    - "Tell me about Dhruv's projects."
    - "Summarize Dhruv's LinkedIn experience."

    Once you've entered all the required keys, the input box below will be enabled.
    """)

    st.markdown("""
    **🔑 How to get your API keys:**

    - [OpenAI Key Guide](https://platform.openai.com/account/api-keys)
    - [Firecrawl Key Guide](https://docs.firecrawl.dev/docs/api/authentication)
    - [Proxycurl Key Guide](https://nubela.co/proxycurl/dashboard)

    📹 YouTube Walkthroughs:
    - [OpenAI Key (YouTube)](https://youtu.be/SzPE_AE0eEo?si=p-NLZLQaTiSwOH3I)
    - [Firecrawl Key (YouTube)](https://youtu.be/noWpWi6IZl4?si=U3x4BZp5f8F8kGyV)
    - [Proxycurl Key (YouTube)](https://youtu.be/1r0COxVMwCc?si=CJTRH_BC1EK4Luuh)
    
        #🔒 **Note:** Your keys and questions are **not stored anywhere**. They are only kept in memory during your current session.
        No data is collected or logged. Once you've entered all the required keys, the input box below will be enabled.

    """)


    st.warning("Please enter all required API keys and profile URLs to use the app.")
    st.stop()







# if user_api_key:
#     llm = ChatOpenAI(model="gpt-4o", api_key=user_api_key)
# else:
#     st.warning("Please enter your OpenAI API Key in the sidebar to continue.")
#     st.stop()


# ------------------------------
# STEP 1: Define state schema using TypedDict
# ------------------------------
class AgentState(TypedDict):
    input: str
    chat_history: List[Dict[str, str]]
    github_response: str
    medium_response: str
    linkedin_response: str
    output: str

initial_state: AgentState = {
    "chat_history": [],
    "input": "",
    "github_response": "",
    "medium_response": "",
    "linkedin_response": "",
    "output": ""
}

# ------------------------------
# STEP 2: Define node functions
# ------------------------------

def github_node(state: AgentState) -> AgentState:
    user_query = state["input"]
    github_response = query_github_agent(user_query, st.session_state.github_profile)
    return {
        **state,
        "github_response": str(github_response)
    }

def medium_node(state: AgentState) -> AgentState:
    user_query = state["input"]
    urls = [url.strip() for url in st.session_state.medium_urls.split(",") if url.strip()]
    if not urls:
        return state  # skip Medium processing
    raw_content = fetch_selected_medium_posts(urls, st.session_state.firecrawl_api_key)
    medium_summary = generate_llm_summary(raw_content, user_query, st.session_state.openai_api_key)
    return {
        **state,
        "medium_response": medium_summary
    }

def linkedin_node(state: AgentState) -> AgentState:
    user_query = state["input"]
    linkedin_summary = generate_linkedin_summary(user_query, st.session_state.linkedin_profile, st.session_state.proxycurl_api_key, st.session_state.openai_api_key)
    return {
        **state,
        "linkedin_response": linkedin_summary
    }

def final_response_node(state: AgentState) -> AgentState:
    user_query = state["input"]
    chat_history = state.get("chat_history", [])

    if st.session_state.openai_api_key:
        llm = ChatOpenAI(model="gpt-4o", api_key=st.session_state.openai_api_key)
    else:
        st.warning("Please enter your OpenAI API Key in the sidebar to continue.")
        st.stop()
    
    github_summary = state.get("github_response", "")
    medium_summary = state.get("medium_response", "")
    linkedin_summary = state.get("linkedin_response", "")

    history_prompt = "\n".join(
        [f"User: {msg['user']}\nAgent: {msg['agent']}" for msg in chat_history]
    )

    full_prompt = (
        f"Previous conversation:\n{history_prompt}\n\n"
        f"Current question: {user_query}\n"
        f"GitHub Info: {github_summary}\n"
        f"Medium Info: {medium_summary}\n"
        f"LinkedIn Info: {linkedin_summary}\n\n"
        f"You are a hepful agent that provides information precisely with details. Try to keep the answers concise but if required provide detailed response in about 200 to 300 words"
    )

    if st.session_state.resume_text:
            full_prompt += f"\nResume Info:\n{resume_text}\n"

    full_prompt += "\nPlease answer concisely and clearly."

    response = llm.invoke(full_prompt).content
    updated_history = chat_history + [{"user": user_query, "agent": response}]
    save_chat_to_supabase(st.session_state.user.email, user_query, response)

    return {
        **state,
        "chat_history": updated_history,
        "output": response
    }

# ------------------------------
# STEP 3: Build the LangGraph
# ------------------------------
graph = StateGraph(AgentState)
graph.add_node("github", github_node)
graph.add_node("medium", medium_node)
graph.add_node("linkedin", linkedin_node)
graph.add_node("final_response", final_response_node)

# Define order of execution
graph.set_entry_point("github")
graph.add_edge("github", "medium")
graph.add_edge("medium", "linkedin")
graph.add_edge("linkedin", "final_response")
graph.set_finish_point("final_response")

personal_agent_with_memory = graph.compile()


def save_chat_to_supabase(email, question, response):
    supabase.table("chat_history").insert({
        "user_email": email,
        "question": question,
        "response": response
    }).execute()


import streamlit as st

# st.set_page_config(page_title="Personal Agent - Ask About a Person", layout="centered")
st.title("👤 Ask About a Person")


# Initialize state
if "state" not in st.session_state:
    st.session_state.state = initial_state.copy()
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# Upload Resume
uploaded_resume = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
if uploaded_resume is not None:
    if uploaded_resume.type == "application/pdf":
        doc = fitz.open(stream=uploaded_resume.read(), filetype="pdf")
        resume_text = "\n".join([page.get_text() for page in doc])
    else:
        resume_text = ""

    st.session_state.resume_text = resume_text
else:
    st.session_state.resume_text = ""

# Show Chat History (on top like ChatGPT)
st.markdown("##### 🗂️ Chat History")
for msg in st.session_state.state.get("chat_history", []):
    with st.chat_message("user"):
        st.markdown(msg["user"])
    with st.chat_message("assistant"):
        st.markdown(msg["agent"])

# Chat Input (at bottom)
user_query = st.chat_input("💬 Ask your question")
send_email_flag = st.checkbox("📩 Email me this response")
user_email = None
if send_email_flag:
    user_email = st.text_input("Enter your email address")

# Main logic
if user_query:
    st.session_state.state["input"] = user_query

    with st.spinner("Thinking..."):
        result = personal_agent_with_memory.invoke(st.session_state.state)
        st.session_state.state = result

        # Display new response
        with st.chat_message("assistant"):
            st.markdown(result["output"])

        # Save chat
        save_chat_to_supabase(
            email=st.session_state.user.email,
            question=user_query,
            response=result["output"]
        )

        # Optionally email response
        if send_email_flag and user_email:
            with st.spinner("Sending email..."):
                subject = "Your Answer from Dhruv's Personal Agent"
                status = send_email(user_email, subject, result["output"])
            if status:
                st.success(f"Email sent to {user_email} ✅")
            else:
                st.error("❌ Failed to send email. Please check your email configuration.")


