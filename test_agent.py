
from tinyfish_client import inspect_career_page

url = "https://jobs.lever.co/weekdayworks"

print("Testing TinyFish Agent...")
print("Career page:", url)

try:
    events = inspect_career_page(
        url=url,
        role="Software Engineering Intern",
        location="India",
    )

    print("\nEvents received:", len(events))

    for event in events:
        print("\n--- AGENT EVENT ---")
        print(event)

except Exception as error:
    print("\nERROR:", type(error).__name__)
    print(error)
