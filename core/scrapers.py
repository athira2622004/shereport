"""
core/scrapers.py
────────────────
Scrapes women/Kerala news from The Hindu, Mathrubhumi, Manorama Online
and saves them into the existing NewsUpdate model.

Install dependencies first:
    pip install requests beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def scrape_the_hindu():
    articles = []
    urls = [
        "https://www.thehindu.com/news/national/kerala/",
        "https://www.thehindu.com/topic/women/",
    ]
    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            for card in soup.select("div.story-card, div.element"):
                title_tag = card.select_one("h3 a, h2 a")
                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)
                link = title_tag.get("href", "")
                if link and not link.startswith("http"):
                    link = "https://www.thehindu.com" + link

                summary_tag = card.select_one("p.intro, p.story-card-text")
                summary = summary_tag.get_text(
                    strip=True) if summary_tag else ""

                img_tag = card.select_one("img")
                image_url = ""
                if img_tag:
                    image_url = img_tag.get(
                        "src") or img_tag.get("data-src") or ""

                if title and link:
                    articles.append({
                        "title":     title,
                        "summary":   summary,
                        "url":       link,
                        "image_url": image_url,
                        "source":    "The Hindu",
                    })
        except Exception as e:
            logger.error(f"[The Hindu] {e}")
    return articles


def scrape_mathrubhumi():
    articles = []
    urls = [
        "https://www.mathrubhumi.com/news/kerala",       # Kerala news
        # Crime news (relevant for SHE Report)
        "https://www.mathrubhumi.com/news/crime",
    ]
    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            for card in soup.select("div.story-list-item, article, div.col-article"):
                title_tag = card.select_one("h1 a, h2 a, h3 a")
                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)
                link = title_tag.get("href", "")
                if link and not link.startswith("http"):
                    link = "https://www.mathrubhumi.com" + link

                summary_tag = card.select_one("p.summary, p.description, p")
                summary = summary_tag.get_text(
                    strip=True) if summary_tag else ""

                img_tag = card.select_one("img")
                image_url = ""
                if img_tag:
                    image_url = img_tag.get(
                        "src") or img_tag.get("data-src") or ""

                if title and link:
                    articles.append({
                        "title":     title,
                        "summary":   summary,
                        "url":       link,
                        "image_url": image_url,
                        "source":    "Mathrubhumi",
                    })
        except Exception as e:
            logger.error(f"[Mathrubhumi] {e}")
    return articles


def scrape_manorama():
    articles = []
    urls = [
        # Kerala news (confirmed working)
        "https://www.onmanorama.com/news/kerala.html",
        "https://www.onmanorama.com/news.html",          # General news
    ]
    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            for card in soup.select("div.story-card, div.om-list-story, article, h2"):
                title_tag = card.select_one("h1 a, h2 a, h3 a, a.title") or (
                    card.find("a") if card.name == "h2" else None
                )
                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)
                link = title_tag.get("href", "")
                if link and not link.startswith("http"):
                    link = "https://www.onmanorama.com" + link

                summary_tag = card.select_one("p.summary, p.intro, p")
                summary = summary_tag.get_text(
                    strip=True) if summary_tag else ""

                img_tag = card.select_one("img")
                image_url = ""
                if img_tag:
                    image_url = img_tag.get(
                        "src") or img_tag.get("data-src") or ""

                if title and link and "onmanorama.com" in link:
                    articles.append({
                        "title":     title,
                        "summary":   summary,
                        "url":       link,
                        "image_url": image_url,
                        "source":    "Manorama Online",
                    })
        except Exception as e:
            logger.error(f"[Manorama] {e}")
    return articles


def fetch_all_news():
    """Collect articles from all 3 sources."""
    results = []
    results.extend(scrape_the_hindu())
    results.extend(scrape_mathrubhumi())
    results.extend(scrape_manorama())
    logger.info(f"Total articles fetched: {len(results)}")
    return results
