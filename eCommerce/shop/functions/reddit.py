import xml.etree.ElementTree as ET

import requests


def get_reddit_posts(subreddit="python"):
    # Build the URL for the subreddit RSS feed
    url = f"https://www.reddit.com/r/{subreddit}/.rss"

    headers = {
        "User-Agent": "DjangoEcommerceApp/1.0"
    }

    # Make the request
    response = requests.get(url, headers=headers)

    # Handle errors
    if response.status_code != 200:
        print("Failed to fetch Reddit posts.")
        print("Status code:", response.status_code)
        return []

    # Parse the XML response
    root = ET.fromstring(response.content)

    posts = []

    # Extract the posts
    for entry in root.findall(
        "{http://www.w3.org/2005/Atom}entry"
    ):
        title = entry.find(
            "{http://www.w3.org/2005/Atom}title"
        ).text

        author = entry.find(
            "{http://www.w3.org/2005/Atom}author/"
            "{http://www.w3.org/2005/Atom}name"
        ).text

        link = entry.find(
            "{http://www.w3.org/2005/Atom}link"
        ).attrib["href"]

        posts.append({
            "title": title,
            "author": author,
            "url": link
        })

    return posts
