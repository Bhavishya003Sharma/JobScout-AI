# 🎯 JobScout AI

**Your AI-powered internship discovery assistant, built with TinyFish.**

JobScout AI helps users discover relevant job and internship opportunities based on their preferred role, location, and keywords. It uses TinyFish Search, Fetch, and Agent APIs to discover opportunities, extract job-page information, and inspect career pages, with a Streamlit interface for interacting with the results.

## ✨ Features

- 🔎 **Role-based search:** Search for opportunities based on your target role.
- 📍 **Location preferences:** Focus your search on a preferred location.
- 🏷️ **Keyword matching:** Improve relevance using skills and keywords.
- 🌐 **Multiple sources:** Discover opportunities from different job websites.
- 🧹 **Deduplication:** Normalize URLs to help remove duplicate listings.
- 📊 **Relevance ranking:** Score and sort matching opportunities.
- 🔗 **Application links:** Access job listings directly from the results.
- 🤖 **Career-page inspection:** Use TinyFish Agent to investigate career pages and extract structured findings.

## 🛠️ Tech Stack

- **Python** for application logic
- **Streamlit** for the user interface
- **TinyFish Search API** for discovering relevant web results
- **TinyFish Fetch API** for extracting webpage content
- **TinyFish Agent API** for browser-based career-page inspection
- **python-dotenv** for environment-variable management
- **Requests** for HTTP communication

## 🔌 How TinyFish Powers JobScout AI

| TinyFish API | Purpose |
|---|---|
| **Search** | Finds relevant job pages and opportunities across the web. |
| **Fetch** | Retrieves webpage content in a structured response for further processing. |
| **Agent** | Navigates and inspects career pages to find relevant openings and return structured findings. |

The application processes search results using filtering, URL normalization, deduplication, and relevance scoring to make the results more useful.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Bhavishya003Sharma/JobScout-AI.git
cd JobScout-AI
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
TINYFISH_API_KEY=your_tinyfish_api_key
```

Replace the placeholder with your own TinyFish API key.

**Security:** Never commit your `.env` file or publish your API key.

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL where you can open JobScout AI in your browser.

## 📁 Project Structure

```text
JobScout-AI/
├── app.py              # Streamlit application
├── tinyfish_client.py  # TinyFish API integrations
├── job_matcher.py      # Filtering, ranking, and deduplication
├── job_finder.py       # Job discovery logic
├── requirements.txt    # Python dependencies
├── test_search.py      # Search API test
├── test_fetch.py       # Fetch API test
├── test_agent.py       # Agent API test
├── test_matcher.py     # Job matcher test
└── .gitignore          # Excludes secrets and local files
```

## 🧪 Testing

The repository includes test scripts for the TinyFish Search, Fetch, and Agent APIs, along with the job-matching logic.

Run an individual test with:

```bash
python test_search.py
python test_fetch.py
python test_agent.py
python test_matcher.py
```

API tests require a valid TinyFish API key and may consume API credits.

## 📚 Documentation

- [TinyFish Search API](https://docs.tinyfish.ai/search-api)
- [TinyFish Fetch API](https://docs.tinyfish.ai/fetch-api)
- [TinyFish Agent API](https://docs.tinyfish.ai/agent-api)

## 🎯 Project Goal

JobScout AI was built for the **TinyFish × TechnoJam bounty**, demonstrating how Search, Fetch, and Agent can work together to simplify job discovery and career-page research.

## 👨‍💻 Author

**Bhavishya Sharma**

- GitHub: [@Bhavishya003Sharma](https://github.com/Bhavishya003Sharma)

---

*Built with Python, Streamlit, and TinyFish.* 🚀
