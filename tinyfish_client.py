
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TINYFISH_API_KEY")

SEARCH_URL = "https://api.search.tinyfish.ai"
FETCH_URL = "https://api.fetch.tinyfish.ai"
AGENT_URL = "https://agent.tinyfish.ai/v1/automation/run-sse"


def get_headers():
    if not API_KEY:
        raise RuntimeError(
            "TINYFISH_API_KEY is missing from your .env file"
        )

    return {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
    }



def search_jobs(role, location, keywords):
    query = f"{role} jobs internships in {location}"

    if keywords:
     query += " " + " ".join(keywords)
    print(f"DEBUG query: {query}")

    response = requests.get(
        SEARCH_URL,
        headers=get_headers(),
        params={"query": query},
        timeout=60,
    )

    print(f"DEBUG HTTP status: {response.status_code}")
    response.raise_for_status()

    data = response.json()

    print(f"DEBUG total_results: {data.get('total_results')}")
    print(f"DEBUG returned_results: {len(data.get('results', []))}")

    return data



def fetch_job_pages(urls):
    response = requests.post(
        FETCH_URL,
        headers=get_headers(),
        json={
            "urls": urls[:10],
            "format": "markdown",
            "ttl": 0,
        },
        timeout=150,
    )

    response.raise_for_status()
    return response.json()


def inspect_career_page(url, role, location):
    goal = f"""
    Find current job or internship openings relevant to:
    Role: {role}
    Location: {location}

    Navigate the career page if necessary.
    Return only real listings found on the website.
    For each listing provide title, company, location,
    description, and direct application URL.
    Do not invent missing information.
    Return structured JSON.
    """

    response = requests.post(
        AGENT_URL,
        headers=get_headers(),
        json={
            "url": url,
            "goal": goal,
        },
        stream=True,
        timeout=(10, 180),
    )

    response.raise_for_status()

    events = []

    for line in response.iter_lines(decode_unicode=True):
        if line and line.startswith("data: "):
            try:
                events.append(json.loads(line[6:]))
            except json.JSONDecodeError:
                continue

    return events
