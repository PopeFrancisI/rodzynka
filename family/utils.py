import re


def slugify(text):
    text: str
    text = text.strip().lower()
    slug: str
    slug = re.sub('[^0-9a-zA-Z]+', '-', text)
    return slug
