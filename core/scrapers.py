"""
core/scrapers.py
────────────────
Scrapes women/Kerala news from 6 sources and saves into NewsUpdate model.

Sources:
  1. The Hindu        - Kerala + Women
  2. Mathrubhumi      - Kerala + Women tag
  3. Manorama Online  - Kerala + Latest
  4. Times of India   - Women topic
  5. Asianet News     - Latest + Kerala
  6. NDTV             - Women in India
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


def _get_soup(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None


def scrape_the_hindu():
    articles = []
    urls = [
        "https://www.thehindu.com/news/national/kerala/",
        "https://www.thehindu.com/topic/women/",
    ]
    for url in urls:
        soup = _get_soup(url)
        if not soup:
            continue
        for card in soup.select("div.story-card, div.element"):
            title_tag = card.select_one("h3 a, h2 a")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href", "")
            if link and not link.startswith("http"):
                link = "https://www.thehindu.com" + link
            summary_tag = card.select_one("p.intro, p.story-card-text")
            summary = summary_tag.get_text(strip=True) if summary_tag else ""
            if title and link:
                articles.append(
                    {"title": title, "summary": summary, "url": link, "source": "The Hindu"})
    return articles


def scrape_mathrubhumi():
    articles = []
    urls = [
        "https://www.mathrubhumi.com/news/kerala",
        "https://www.mathrubhumi.com/topics/tag/women",
    ]
    for url in urls:
        soup = _get_soup(url)
        if not soup:
            continue
        for card in soup.select("div.story-list-item, article, div.col-article"):
            title_tag = card.select_one("h1 a, h2 a, h3 a")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href", "")
            if link and not link.startswith("http"):
                link = "https://www.mathrubhumi.com" + link
            summary_tag = card.select_one("p.summary, p.description, p")
            summary = summary_tag.get_text(strip=True) if summary_tag else ""
            if title and link:
                articles.append(
                    {"title": title, "summary": summary, "url": link, "source": "Mathrubhumi"})
    return articles


def scrape_manorama():
    articles = []
    urls = [
        "https://www.manoramaonline.com/news/latest-news.html",
        "https://www.onmanorama.com/news/kerala.html",
    ]
    for url in urls:
        soup = _get_soup(url)
        if not soup:
            continue
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
            summary = summary_tag.get_text(strip=True) if summary_tag else ""
            if title and link and ("onmanorama.com" in link or "manoramaonline.com" in link):
                articles.append(
                    {"title": title, "summary": summary, "url": link, "source": "Manorama Online"})
    return articles


def scrape_times_of_india():
    articles = []
    url = "https://timesofindia.indiatimes.com/topic/women"
    soup = _get_soup(url)
    if not soup:
        return articles
    for card in soup.select("div.uwU81, div.iN3cm, li.article"):
        title_tag = card.select_one("a.wjfZO, a.xXa29, h3 a, h2 a, a")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")
        if link and not link.startswith("http"):
            link = "https://timesofindia.indiatimes.com" + link
        summary_tag = card.select_one("p, div.oxXSK")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        if title and link and len(title) > 10:
            articles.append({"title": title, "summary": summary,
                            "url": link, "source": "Times of India"})
    return articles


def scrape_asianet():
    articles = []
    urls = [
        "https://www.asianetnews.com/latest-news",
        "https://www.asianetnews.com/kerala-news",
    ]
    for url in urls:
        soup = _get_soup(url)
        if not soup:
            continue
        for card in soup.select("a[href*='/kerala-news/'], a[href*='/crime-news/'], a[href*='/india-news/']"):
            title = card.get_text(strip=True)
            link = card.get("href", "")
            if link and not link.startswith("http"):
                link = "https://www.asianetnews.com" + link
            if title and link and len(title) > 15:
                articles.append({"title": title, "summary": "",
                                "url": link, "source": "Asianet News"})
    return articles


def scrape_ndtv():
    articles = []
    url = "https://www.ndtv.com/topic/women-in-india"
    soup = _get_soup(url)
    if not soup:
        return articles
    for card in soup.select("div.news_Itm, div.nwscntnr, div.story__list-item, article"):
        title_tag = card.select_one("h2 a, h3 a, a.newsHdng")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")
        if link and not link.startswith("http"):
            link = "https://www.ndtv.com" + link
        summary_tag = card.select_one("p, div.newsCont")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        if title and link and len(title) > 10:
            articles.append({"title": title, "summary": summary,
                            "url": link, "source": "NDTV"})
    return articles


def fetch_all_news():
    """Collect articles from all 6 sources."""
    results = []
    results.extend(scrape_the_hindu())
    results.extend(scrape_mathrubhumi())
    results.extend(scrape_manorama())
    results.extend(scrape_times_of_india())
    results.extend(scrape_asianet())
    results.extend(scrape_ndtv())
    logger.info(f"Total articles fetched: {len(results)}")
    return results
