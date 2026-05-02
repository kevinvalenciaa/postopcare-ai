"""POC-009: Clinical guidelines scraper.

Pulls post-op guideline pages from medical society websites and writes
structured records (title, url, organization, content). Respects
robots.txt and rate-limits at 2s between requests per host.
"""

from __future__ import annotations

import json
import logging
import time
import urllib.robotparser
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

USER_AGENT = "PostOpCareBot/0.1 (+https://postopcare.ca)"
RATE_LIMIT_SECONDS = 2.0


@dataclass
class GuidelineDoc:
    title: str
    url: str
    organization: str
    procedure: Optional[str]
    pub_date: Optional[str]
    content: str

    def to_dict(self) -> dict:
        return asdict(self)


def _can_fetch(url: str) -> bool:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
    except Exception as e:
        logger.warning("Could not read robots.txt at %s: %s — proceeding cautiously", robots_url, e)
        return True
    return rp.can_fetch(USER_AGENT, url)


_last_request_time: dict[str, float] = {}


def _rate_limit(host: str) -> None:
    now = time.time()
    last = _last_request_time.get(host, 0.0)
    wait = RATE_LIMIT_SECONDS - (now - last)
    if wait > 0:
        time.sleep(wait)
    _last_request_time[host] = time.time()


def fetch(url: str) -> Optional[str]:
    """Fetch HTML respecting robots.txt and rate limits. Returns None on disallow/error."""
    if not _can_fetch(url):
        logger.warning("robots.txt disallows %s", url)
        return None
    host = urlparse(url).netloc
    _rate_limit(host)
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        logger.error("Fetch failed for %s: %s", url, e)
        return None


def parse_guideline_page(html: str, url: str, organization: str, procedure: Optional[str] = None) -> Optional[GuidelineDoc]:
    """Generic extractor: title from <h1>/<title>, body from <article> or <main>.

    Each medical-society site has its own DOM; this is the fallback. Add
    site-specific selectors below as needed.
    """
    soup = BeautifulSoup(html, "html.parser")
    title = ""
    if soup.h1:
        title = soup.h1.get_text(strip=True)
    elif soup.title:
        title = soup.title.get_text(strip=True)
    body = soup.find("article") or soup.find("main") or soup.body
    if body is None:
        return None
    for tag in body(["script", "style", "nav", "footer", "aside"]):
        tag.decompose()
    content = body.get_text(separator="\n", strip=True)
    if len(content) < 200:
        return None
    return GuidelineDoc(
        title=title or url,
        url=url,
        organization=organization,
        procedure=procedure,
        pub_date=None,
        content=content,
    )


GUIDELINE_SOURCES: list[dict] = [
    # AAOS — Orthopedic
    {"organization": "AAOS", "procedure": "total-knee-replacement",
     "url": "https://www.aaos.org/quality/quality-programs/lower-extremity-programs/surgical-management-of-osteoarthritis-of-the-knee/"},
    {"organization": "AAOS", "procedure": "total-hip-replacement",
     "url": "https://orthoinfo.aaos.org/en/treatment/total-hip-replacement/"},
    {"organization": "AAOS", "procedure": "acl-reconstruction",
     "url": "https://orthoinfo.aaos.org/en/treatment/acl-injury-does-it-require-surgery/"},
    # ACOG — OB/GYN
    {"organization": "ACOG", "procedure": "cesarean-section",
     "url": "https://www.acog.org/womens-health/faqs/cesarean-birth"},
    # ACS — General Surgery
    {"organization": "ACS", "procedure": "laparoscopic-cholecystectomy",
     "url": "https://www.facs.org/for-patients/recovering-from-surgery/"},
]


def scrape_all(output_path: Optional[Path] = None) -> list[GuidelineDoc]:
    """Scrape every entry in GUIDELINE_SOURCES. Returns successful records."""
    docs: list[GuidelineDoc] = []
    for src in GUIDELINE_SOURCES:
        html = fetch(src["url"])
        if not html:
            continue
        doc = parse_guideline_page(html, src["url"], src["organization"], src.get("procedure"))
        if doc:
            docs.append(doc)
            logger.info("Scraped %s — %d chars", src["url"], len(doc.content))
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump([d.to_dict() for d in docs], f, indent=2)
        logger.info("Wrote %d guidelines to %s", len(docs), output_path)
    return docs


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    out = Path("data/guidelines.json")
    docs = scrape_all(output_path=out)
    print(f"Scraped {len(docs)} guidelines from {len({d.organization for d in docs})} organizations.")
