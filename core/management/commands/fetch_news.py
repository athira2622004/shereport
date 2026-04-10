"""
core/management/commands/fetch_news.py
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import NewsUpdate
from core.scrapers import fetch_all_news


class Command(BaseCommand):
    help = "Auto-fetch news from The Hindu, Mathrubhumi, Manorama Online"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print articles without saving to database",
        )

    def handle(self, *args, **options):
        self.stdout.write("Fetching news articles...")

        articles = fetch_all_news()
        new_count = 0
        skipped = 0

        for item in articles:
            if not item.get("title") or not item.get("url"):
                continue

            safe_url = item["url"][:200]

            if options["dry_run"]:
                self.stdout.write(f"  [{item['source']}] {item['title'][:80]}")
                continue

            # Skip duplicates
            if NewsUpdate.objects.filter(url=safe_url).exists():
                skipped += 1
                continue

            NewsUpdate.objects.create(
                title=item["title"][:300],
                summary=item.get("summary", ""),
                source=item.get("source", ""),
                url=safe_url,
                image_url=item.get("image_url", "")[
                    :500],  # ← external image URL
                date_published=timezone.now().date(),
                is_active=False,
            )
            new_count += 1

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING(
                "Dry-run done. Nothing saved."))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Done — {new_count} new article(s) saved, "
                f"{skipped} duplicate(s) skipped.\n"
                f"Go to Django Admin > News Updates to review and publish."
            ))
