# # linkedin_agent.py

import requests
from langchain.chat_models import ChatOpenAI

def extract_clean_summary(profile):
    name = profile.get("full_name", "")
    headline = profile.get("headline", "")
    occupation = profile.get("occupation", "")
    location = f"{profile.get('city', '')}, {profile.get('state', '')}"
    summary = profile.get("summary", "")
    experience = profile.get("experiences", [])
    education = profile.get("education", [])
    
    experience_str = "\n".join(
        f"- {exp.get('title', '')} at {exp.get('company', '')} ({exp.get('starts_at', {}).get('year', '')})"
        for exp in experience
    )

    education_str = "\n".join(
        f"- {edu.get('degree_name', '')} in {edu.get('field_of_study', '')} at {edu.get('school', '')} ({edu.get('starts_at', {}).get('year', '')})"
        for edu in education
    )

    clean_text = f"""
Name: {name}
Headline: {headline}
Occupation: {occupation}
Location: {location}

Summary:
{summary}

Experience:
{experience_str}

Education:
{education_str}
""".strip()
    return clean_text


def generate_linkedin_summary(question: str, linkedin_url: str, proxycurl_api_key: str, openai_api_key: str) -> str:
    headers = {'Authorization': 'Bearer ' + proxycurl_api_key}
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    params = {
        'linkedin_profile_url': linkedin_url,
        'personal_contact_number': 'include',
        'personal_email': 'include',
        'skills': 'include',
        'use_cache': 'if-present',
        'fallback_to_cache': 'on-error',
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=headers)

    if response.status_code == 200:
        profile_data = response.json()
        clean_profile = extract_clean_summary(profile_data)

        prompt = (
            "You are a helpful assistant that answers questions strictly based on the LinkedIn profile below. "
            "Do not assume anything. If the answer is not present, say 'Not enough information available.'\n\n"
            f"LinkedIn Profile:\n{clean_profile}\n\n"
            f"User Question: {question}\n\n"
            "Answer:"
        )

        llm = ChatOpenAI(model="gpt-4", api_key=openai_api_key)
        return llm.invoke(prompt)
    else:
        return f"Request failed with status code {response.status_code}"
