import os
from datetime import datetime
from html.parser import HTMLParser

import django
import feedparser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return "".join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def strp_datetime(datetime_str):
    fmts = ["%Y-%m-%dT%H:%M:%S%fZ", "%Y-%m-%dT%H:%M:%S.%fZ", "%a, %d %b %Y %H:%M:%S %z"]
    for fmt in fmts:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            pass
    raise ValueError("no valid date format found")


def fetch(url):
    from core.models import Post

    d = feedparser.parse(url)
    entries = d.entries
    for entry in entries:
        try:
            content = entry.content and entry.content[0].value
        except AttributeError:
            content = entry.summary or entry.title
        try:
            created_at = strp_datetime(entry.published)
        except ValueError:
            print(entry.published)
            created_at = None
        try:
            tags = entry.tags
        except AttributeError:
            tags = []

        _, ok = Post.update_or_create(
            author_id=2,
            title=entry.title,
            orig_url=entry.link,
            content=strip_tags(content),
            created_at=created_at,
            tags=[tag.term for tag in tags],
        )


def main():
    profile = os.environ.get("ITOUTIAO_PROFILE", "develop")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{profile}")
    django.setup()

    from core.models import PostTag, Post, Tag

    for model in (Post, PostTag, Tag):
        model.objects.all().delete()

    for site in ("http://127.0.0.1:8000/feed",):
        fetch(site)


if __name__ == "__main__":
    main()
