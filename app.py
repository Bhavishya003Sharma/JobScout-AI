
import html
import streamlit as st

from tinyfish_client import (
    search_jobs,
    fetch_job_pages,
    inspect_career_page,
)
from job_matcher import prepare_jobs


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="JobScout AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown(
    """
    <style>
    :root {
        --background: #0b1020;
        --surface: #111a2e;
        --surface-hover: #17223a;
        --border: #283650;
        --text: #f1f5f9;
        --muted: #a5b4cc;
        --accent: #818cf8;
        --accent-strong: #6366f1;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(99, 102, 241, 0.13),
                transparent 30%
            ),
            var(--background);
        color: var(--text);
    }

    .block-container {
        max-width: 1320px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: #0e1628;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: var(--text) !important;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 8px;
    }

    .brand-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 56px;
        height: 56px;
        border-radius: 16px;
        font-size: 29px;
        background: linear-gradient(
            135deg,
            #6366f1,
            #8b5cf6
        );
        box-shadow: 0 8px 28px rgba(99, 102, 241, 0.28);
    }

    .brand-title {
        color: #f8fafc;
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1.2px;
        line-height: 1.2;
    }

    .brand-subtitle {
        color: var(--muted);
        font-size: 15px;
        margin-top: 8px;
        margin-bottom: 26px;
    }

    .section-heading {
        color: #f1f5f9;
        font-size: 22px;
        font-weight: 750;
        margin: 24px 0 4px;
    }

    .section-subtitle {
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 18px;
    }

    .job-card {
        background: linear-gradient(
            145deg,
            #141f35,
            #10182a
        );
        border: 1px solid var(--border);
        border-radius: 17px;
        padding: 23px;
        margin: 12px 0 18px;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.13);
        transition: border-color 0.2s ease,
                    transform 0.2s ease;
    }

    .job-card:hover {
        border-color: #6366f1;
        transform: translateY(-2px);
    }

    .job-card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 14px;
        flex-wrap: wrap;
    }

    .job-number {
        color: #818cf8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 7px;
    }

    .job-title {
        color: #f8fafc;
        font-size: 21px;
        font-weight: 750;
        line-height: 1.45;
        overflow-wrap: anywhere;
    }

    .match-badge {
        white-space: nowrap;
        color: #c4b5fd;
        background: rgba(139, 92, 246, 0.13);
        border: 1px solid rgba(139, 92, 246, 0.35);
        border-radius: 999px;
        padding: 7px 11px;
        font-size: 12px;
        font-weight: 700;
    }

    .job-source {
        display: inline-block;
        color: #cbd5e1;
        background: #202c42;
        border: 1px solid #33425d;
        padding: 5px 9px;
        border-radius: 7px;
        font-size: 12px;
        margin-top: 13px;
    }

    .job-description {
        color: #c4cedf;
        font-size: 14px;
        line-height: 1.8;
        margin-top: 17px;
        margin-bottom: 19px;
        overflow-wrap: anywhere;
    }

    .job-link {
        display: inline-block;
        color: white !important;
        background: linear-gradient(
            100deg,
            #6366f1,
            #8b5cf6
        );
        text-decoration: none !important;
        padding: 10px 15px;
        border-radius: 9px;
        font-size: 13px;
        font-weight: 650;
    }

    .job-link:hover {
        filter: brightness(1.12);
    }

    .metric-card {
        background: #111a2e;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 17px;
        min-height: 88px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 7px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 23px;
        font-weight: 750;
    }

    .stTextInput input {
        background: #141f35;
        color: #f8fafc;
        border: 1px solid #34435f;
        border-radius: 10px;
    }

    .stTextInput input:focus {
        border-color: #818cf8;
        box-shadow: 0 0 0 1px #818cf8;
    }

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #818cf8;
        color: #c7d2fe;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    a {
        color: #a5b4fc;
    }

    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">🎯</div>
        <div class="brand-title">JobScout AI</div>
    </div>
    <div class="brand-subtitle">
        Discover opportunities that match your skills.
        Powered by TinyFish Search, Fetch, and Agent.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR: USER PREFERENCES
# =========================================================

with st.sidebar:
    st.markdown("## ⚙️ Your preferences")
    st.caption("Personalize your internship search.")

    role = st.text_input(
        "Target role",
        value="Software Engineering Intern",
        key="role_input",
    )

    location = st.text_input(
        "Preferred location",
        value="India",
        key="location_input",
    )

    keyword_text = st.text_input(
        "Skills / keywords",
        value="Python, C++, DSA",
        help="Separate keywords with commas.",
        key="keyword_input",
    )

    search_button = st.button(
        "🔎  Find internships",
        type="primary",
        use_container_width=True,
    )

    st.divider()

    st.caption("Built with TinyFish APIs")


# =========================================================
# SEARCH API
# =========================================================

if search_button:
    if not role.strip() or not location.strip():
        st.error("Please enter both a target role and a location.")
    else:
        keywords = [
            word.strip()
            for word in keyword_text.split(",")
            if word.strip()
        ]

        with st.spinner("Searching for matching opportunities..."):
            try:
                response = search_jobs(
                    role=role.strip(),
                    location=location.strip(),
                    keywords=keywords,
                )

                jobs = prepare_jobs(
                    [response],
                    role=role.strip(),
                    location=location.strip(),
                    keywords=keywords,
                )

                st.session_state["jobs"] = jobs
                st.session_state["search_role"] = role.strip()
                st.session_state["search_location"] = location.strip()
                st.session_state["search_keywords"] = keywords

            except Exception as error:
                st.error(
                    f"Search failed: {type(error).__name__}: {error}"
                )


# =========================================================
# SEARCH RESULTS
# =========================================================

jobs = st.session_state.get("jobs", [])

if jobs:
    st.markdown(
        '<div class="section-heading">✨ Matched opportunities</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Results ranked by your selected role and keywords. '
        'Verify vacancy details on the original source.'
        '</div>',
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(3)

    metrics = [
        ("SEARCH RESULTS", str(len(jobs))),
        ("TARGET ROLE", st.session_state.get("search_role", role)),
        ("LOCATION", st.session_state.get("search_location", location)),
    ]

    for col, (label, value) in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{html.escape(str(label))}</div>
                    <div class="metric-value"
                         style="font-size:18px; overflow-wrap:anywhere;">
                        {html.escape(str(value))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    for index, job in enumerate(jobs, start=1):
        title = str(job.get("title") or "Untitled position")
        source = str(job.get("source") or "Unknown source")
        score = job.get("score", "N/A")
        snippet = str(
            job.get("snippet") or "No description provided by the source."
        )
        url = str(job.get("url") or "")

        safe_title = html.escape(title)
        safe_source = html.escape(source)
        safe_snippet = html.escape(snippet)
        safe_url = html.escape(url, quote=True)

        link_html = ""
        if url.startswith(("https://", "http://")):
            link_html = (
                f'<a class="job-link" href="{safe_url}" '
                'target="_blank" rel="noopener noreferrer">'
                "↗ View original listing</a>"
            )

        
        card_html = f"""
<div class="job-card">
    <div class="job-card-top">
        <div style="flex:1; min-width:220px;">
            <div class="job-number">OPPORTUNITY {index:02d}</div>
            <div class="job-title">{safe_title}</div>
        </div>
        <div class="match-badge">✦ Match score: {html.escape(str(score))}</div>
    </div>
    <div class="job-source">🌐 {safe_source}</div>
    <div class="job-description">{safe_snippet}</div>
    {link_html}
</div>
"""

        st.markdown(card_html, unsafe_allow_html=True)

         

        # -------------------------------------------------
        # ACTIONS
        # -------------------------------------------------

        action_fetch, action_agent = st.columns(2)

        # -------------------------------------------------
        # FETCH API
        # -------------------------------------------------

        with action_fetch:
            if st.button(
                "📄 Fetch job details",
                key=f"fetch_{index}",
                use_container_width=True,
            ):
                if not url:
                    st.warning("This result has no URL to fetch.")
                else:
                    with st.spinner("Fetching job-page content..."):
                        try:
                            fetched = fetch_job_pages([url])

                            results = fetched.get("results", [])
                            errors = fetched.get("errors", [])

                            if results:
                                page = results[0]

                                with st.expander(
                                    f"📄 Job details: {title}",
                                    expanded=True,
                                ):
                                    st.markdown(
                                        f"### {page.get('title') or title}"
                                    )

                                    final_url = (
                                        page.get("final_url")
                                        or page.get("url")
                                        or url
                                    )

                                    if final_url.startswith(
                                        ("https://", "http://")
                                    ):
                                        st.markdown(
                                            f"[Open source page]({final_url})"
                                        )

                                    description = str(
                                        page.get("description") or ""
                                    ).strip()

                                    page_text = str(
                                        page.get("text") or ""
                                    ).strip()

                                    content = description or page_text

                                    if content:
                                        st.text_area(
                                            "Extracted page content",
                                            value=content[:10000],
                                            height=280,
                                            key=f"fetch_content_{index}",
                                        )
                                    else:
                                        st.info(
                                            "Fetch returned no readable content."
                                        )
                            else:
                                st.warning(
                                    "Fetch returned no page content."
                                )
                                if errors:
                                    st.caption(str(errors))

                        except Exception as error:
                            st.error(
                                f"Fetch failed: "
                                f"{type(error).__name__}: {error}"
                            )

        # -------------------------------------------------
        # AGENT API
        # -------------------------------------------------

        with action_agent:
            if st.button(
                "🤖 Inspect with Agent",
                key=f"agent_{index}",
                use_container_width=True,
            ):
                if not url:
                    st.warning("This result has no URL to inspect.")
                else:
                    with st.spinner(
                        "TinyFish Agent is inspecting this page..."
                    ):
                        try:
                            events = inspect_career_page(
                                url=url,
                                role=st.session_state.get(
                                    "search_role", role
                                ),
                                location=st.session_state.get(
                                    "search_location", location
                                ),
                            )

                            complete_events = [
                                event
                                for event in events
                                if event.get("type") == "COMPLETE"
                            ]

                            if not complete_events:
                                st.warning(
                                    "No completed Agent result was returned. "
                                    "Check the terminal for errors."
                                )
                            else:
                                complete_event = complete_events[-1]
                                status = complete_event.get("status")

                                if status not in (None, "COMPLETED"):
                                    st.error(
                                        f"Agent status: {status}"
                                    )
                                    continue_display = False
                                else:
                                    continue_display = True

                                if continue_display:
                                    result = (
                                        complete_event.get("result") or {}
                                    )

                                    with st.expander(
                                        f"🤖 Agent findings: {title}",
                                        expanded=True,
                                    ):
                                        query_info = result.get("query", {})
                                        filters = result.get(
                                            "searched_filters", {}
                                        )

                                        st.caption(
                                            "Role: "
                                            + str(
                                                query_info.get("role")
                                                or st.session_state.get(
                                                    "search_role", role
                                                )
                                            )
                                            + " · Location: "
                                            + str(
                                                query_info.get("location")
                                                or filters.get("location")
                                                or st.session_state.get(
                                                    "search_location", location
                                                )
                                            )
                                        )

                                        message = result.get("message")
                                        if message:
                                            st.write(message)

                                        listings = result.get("listings", [])
                                        if not isinstance(listings, list):
                                            listings = []

                                        findings = result.get("findings", {})

                                        if isinstance(findings, dict):
                                            for category in findings.values():
                                                if not isinstance(
                                                    category, dict
                                                ):
                                                    continue

                                                openings = category.get(
                                                    "openings", []
                                                )

                                                if isinstance(openings, list):
                                                    listings.extend(openings)

                                        unique_listings = []
                                        seen_listings = set()

                                        for item in listings:
                                            if not isinstance(item, dict):
                                                continue

                                            application_url = (
                                                item.get("application_url")
                                                or item.get("apply_url")
                                                or item.get("url")
                                                or ""
                                            )

                                            if application_url:
                                                identity = application_url.strip().lower()
                                            else:
                                                identity = (
                                                    str(item.get("title", "")).strip().lower(),
                                                    str(item.get("company", "")).strip().lower(),
                                                )

                                            if identity in seen_listings:
                                                continue

                                            seen_listings.add(identity)
                                            unique_listings.append(item)

                                        if unique_listings:
                                            st.success(
                                                f"{len(unique_listings)} "
                                                "listing(s) found."
                                            )

                                            for item in unique_listings:
                                                with st.container(border=True):
                                                    st.markdown(
                                                        "#### "
                                                        + str(
                                                            item.get(
                                                                "title",
                                                                "Untitled position",
                                                            )
                                                        )
                                                    )

                                                    st.caption(
                                                        str(
                                                            item.get(
                                                                "company",
                                                                "Company not provided",
                                                            )
                                                        )
                                                        + " · "
                                                        + str(
                                                            item.get(
                                                                "location",
                                                                "Location not provided",
                                                            )
                                                        )
                                                    )

                                                    st.write(
                                                        item.get("description")
                                                        or item.get("snippet")
                                                        or "No description provided."
                                                    )

                                                    if application_url:
                                                        pass

                                                    listing_url = (
                                                        item.get("application_url")
                                                        or item.get("apply_url")
                                                        or item.get("url")
                                                    )

                                                    if listing_url and str(
                                                        listing_url
                                                    ).startswith(
                                                        ("https://", "http://")
                                                    ):
                                                        st.markdown(
                                                            f"[↗ Apply for this job]({listing_url})"
                                                        )
                                        else:
                                            conclusion = (
                                                result.get("conclusion")
                                                or result.get("note")
                                                or "No matching openings were found on this page."
                                            )
                                            st.info(conclusion)

                                        if filters:
                                            with st.expander(
                                                "Inspection filters"
                                            ):
                                                st.write(filters)
                        except Exception as error:
                            st.error(
                                f"Agent failed: "
                                f"{type(error).__name__}: {error}"
                            )

    st.caption(
        "Search results are leads, not guarantees of active vacancies. "
        "Confirm availability and eligibility on the original listing."
    )

elif search_button:
    st.warning(
        "No matching listings were returned. "
        "Try a broader role or fewer keywords."
    )

else:
    st.markdown(
        """
        <div class="job-card" style="text-align:center; padding:45px 24px;">
            <div style="font-size:42px; margin-bottom:12px;">🔎</div>
            <div class="job-title">Your next opportunity starts here</div>
            <div class="job-description">
                Enter your target role, location, and skills in the sidebar,
                then click Find internships to discover matching opportunities.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
