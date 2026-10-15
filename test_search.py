
from tinyfish_client import search_jobs
import requests

print("Running one TinyFish Search request...")

try:
    data = search_jobs(
        role="Python Developer Intern",
        location="India",
        keywords=["Python"],
    )

    print("\nQuery:", data.get("query"))
    print("Total results:", data.get("total_results"))
    print("Returned results:", len(data.get("results", [])))
    print("First result:", data.get("results", [{}])[0])

except requests.HTTPError as error:
    print("HTTP error:", error)
    if error.response is not None:
        print("Status:", error.response.status_code)
        print("Response:", error.response.text[:1000])

except Exception as error:
    print("Error:", type(error).__name__, error)
