
from tinyfish_client import search_jobs
from job_matcher import prepare_jobs

role = "Software Engineering Intern"
location = "India"
keywords = ["Python", "C++", "DSA"]

print("Searching TinyFish...")

response = search_jobs(
    role=role,
    location=location,
    keywords=keywords,
)

print("Search results received:", len(response.get("results", [])))

jobs = prepare_jobs(
    [response],
    role=role,
    location=location,
    keywords=keywords,
)

print(f"\nJobs after filtering: {len(jobs)}")

for index, job in enumerate(jobs[:10], start=1):
    print(f"\n{index}. {job['title']}")
    print("Match score:", job["score"])
    print("Source:", job["source"])
    print("Apply URL:", job["url"])
    print("Details:", job["snippet"][:200])
