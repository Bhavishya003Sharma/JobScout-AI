
import re
from urllib.parse import urlsplit, urlunsplit


def clean_text(value):
    """Normalize text so matching is consistent."""
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_url(url):
    """Remove query parameters and fragments for deduplication."""
    url = clean_text(url)

    if not url.startswith(("http://", "https://")):
        return ""

    parts = urlsplit(url)

    if not parts.netloc:
        return ""

    return urlunsplit((
        parts.scheme.lower(),
        parts.netloc.lower(),
        parts.path.rstrip("/"),
        "",
        "",
    ))


def prepare_jobs(search_responses, role, location, keywords):
    """Clean, deduplicate, filter, and rank search results."""

    jobs_by_url = {}

    role_terms = [
        word.lower()
        for word in re.findall(r"[a-zA-Z0-9+#.]+", role)
        if len(word) > 1
    ]

    location_text = clean_text(location).lower()

    keywords = [
        clean_text(word).lower()
        for word in keywords
        if clean_text(word)
    ]

    # Titles that usually indicate directories or articles,
    # rather than individual job opportunities.
    generic_title_patterns = [
        r"\bjobs in\b",
        r"\bjobs (?=for\b)",
        r"\bjob search\b",
        r"\bsearch jobs\b",
        r"\ball openings\b",
        r"\bpositions archive\b",
        r"\binternship opportunities\b",
        r"\binternships\b.*\btimeline\b",
        r"\bcareer opportunities\b",
        r"\bjob listings\b",
        r"\bopen roles\b",
        r"\bjobs and internships\b",
    ]

    for response in search_responses:
        if not isinstance(response, dict):
            continue

        results = response.get("results", [])

        if not isinstance(results, list):
            continue

        for result in results:
            if not isinstance(result, dict):
                continue

            title = clean_text(result.get("title"))
            snippet = clean_text(result.get("snippet"))
            url = normalize_url(result.get("url"))
            source = clean_text(result.get("site_name"))

            if not title or not url:
                continue

            title_lower = title.lower()
            text = f"{title} {snippet}".lower()
            full_text = f"{title} {snippet} {url}".lower()

            # Remove obvious generic pages and articles.
            if any(
                re.search(pattern, title_lower)
                for pattern in generic_title_patterns
            ):
                continue

            # Give individual roles a stronger score than generic results.
            score = 0

            for term in role_terms:
                if term in title_lower:
                    score += 3
                elif term in text:
                    score += 1

            for keyword in keywords:
                if keyword in text:
                    score += 2

            # Prefer results that mention the requested location.
            if location_text and location_text in full_text:
                score += 3

            # Penalize explicit location mismatches when the result
            # mentions a different country or region.
            #
            # This is a conservative heuristic, not proof of the job's
            # actual location. Search snippets may omit location details.
            location_mismatch = False

            if location_text in {"us", "usa", "united states"}:
                foreign_location_terms = [
                    "india",
                    "united kingdom",
                    "uk-based",
                    "canada",
                    "australia",
                    "germany",
                ]

                location_mismatch = any(
                    term in text for term in foreign_location_terms
                )

            elif location_text == "india":
                foreign_location_terms = [
                    "united states",
                    "u.s.",
                    "canada",
                    "united kingdom",
                    "uk-based",
                    "australia",
                ]

                location_mismatch = any(
                    term in text for term in foreign_location_terms
                )

            if location_mismatch:
                score -= 5

            job = {
                "title": title,
                "snippet": snippet,
                "url": url,
                "source": source,
                "score": score,
            }

            # Keep only one result per normalized URL.
            existing = jobs_by_url.get(url)

            if existing is None or score > existing["score"]:
                jobs_by_url[url] = job

    ranked_jobs = sorted(
        jobs_by_url.values(),
        key=lambda job: job["score"],
        reverse=True,
    )

    return ranked_jobs
