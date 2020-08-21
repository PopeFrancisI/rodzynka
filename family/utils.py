import re


def slugify(text):
    text = text.strip().lower()
    slug = re.sub('[^0-9a-zA-Z]+', '-', text)
    return slug
