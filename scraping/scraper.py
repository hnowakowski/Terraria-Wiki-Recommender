import bs4
import requests
import re
from time import sleep
from random import random
import cloudscraper

# can be some template pages if they ever pop up
URL_BLACKLIST = []

URL = "https://terraria.wiki.gg"

def get_url(url, scraper):
    headers = {
    "User-Agent": "Chrome/141.0.0.0"
    }
    res = scraper.get(url, headers=headers)
    if res.status_code != 200:
        print(f"WARNING! Get request returned code other than 200: {res.status_code}")
    print(res.status_code)
    return res.text

def bfs(initial_pages, iterations):
    all_pages = initial_pages[:]
    queue = initial_pages
    while iterations:
        curr = get_url(URL + queue.pop(0).get("href"))
        soup = bs4.BeautifulSoup(curr.text, "html.parser")
        print(curr.text)
        with open("test.txt", "w") as f:
            f.write(curr.text)
        body = soup.find("div", {"class": "mw-content-ltr mw-parser-output flash-anchored"})
        hyperlinks = [a for a in body.find_all("a", attrs={'href': re.compile(r'^/wiki')}) if not a.find("img")]
        for link in hyperlinks:
            if link not in all_pages:
                all_pages.append(link)
                queue.append(link)
        iterations -= 1
    return all_pages



def scrape():
    scraper = cloudscraper.CloudScraper()
    main_site = get_url(URL, scraper)
    # id="main-section" <-- extract all wiki.gg hrefs from here and start bfs
    # h1 id="firstHeading" (page title) div class="mw-content-ltr mw-parser-output flash-anchored" (body) <--- for other pages
    soup = bs4.BeautifulSoup(main_site, "html.parser")
    body = soup.find("div", {"id": "main-section"})
    hyperlinks = [a for a in body.find_all("a", attrs={'href': re.compile(r'^/wiki')}) if not a.find("img")]
    for link in hyperlinks:
        print(link, ": ", link.get("href"))
        get_url(URL + link.get("href"), scraper)
        sleep(10*random())
    print("yeah")
    sleep(5)
    all_pages = bfs(hyperlinks, 1)

