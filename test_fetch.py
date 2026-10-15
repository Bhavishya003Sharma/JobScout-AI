
from tinyfish_client import fetch_job_pages

url = (
    "https://jobs.lever.co/weekdayworks/"
    "a86efff4-1c2e-43fc-8ecb-dc8f873db2f1"
)

print("Testing TinyFish Fetch...")
print("URL:", url)

try:
    data = fetch_job_pages([url])

    print("\nResponse keys:", list(data.keys()))

    results = data.get("results", [])
    errors = data.get("errors", [])

    print("Pages fetched:", len(results))
    print("Fetch errors:", len(errors))

    for page in results:
        print("\n--- FETCHED PAGE ---")
        print("Title:", page.get("title"))
        print("URL:", page.get("url"))
        print("Final URL:", page.get("final_url"))

        content = page.get("text") or ""
        print("\nExtracted content:")
        print(content[:3000])
        print("\nAll returned fields:")
        print(page.keys())

    if errors:
        print("\n--- FETCH ERRORS ---")
        for error in errors:
            print(error)

except Exception as error:
    print("\nERROR:", type(error).__name__)
    print(error)
