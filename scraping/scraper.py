import bs4
import requests
import re
from time import sleep
from random import random

# can be some template pages if they ever pop up
URL_BLACKLIST = []

URL = "https://terraria.wiki.gg"

def get_url(url, session):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Referer": URL
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"WARNING! Get request returned code other than 200: {res.status_code}")
    return res

def bfs(initial_pages, session, iterations):
    all_pages = initial_pages[:]
    queue = initial_pages
    while iterations:
        curr = get_url(URL + queue.pop(0).get("href"), session)
        soup = bs4.BeautifulSoup(curr, "html.parser")
        print(curr)
        with open("test.txt", "w") as f:
            f.write(curr)
        body = soup.find("div", {"class": "mw-content-ltr mw-parser-output flash-anchored"})
        hyperlinks = [a for a in body.find_all("a", attrs={'href': re.compile(r'^/wiki')}) if not a.find("img")]
        for link in hyperlinks:
            if link not in all_pages:
                all_pages.append(link)
                queue.append(link)
        iterations -= 1
    return all_pages





def scrape():
    session = requests.Session()
    main_site = get_url(URL, session)
    # id="main-section" <-- extract all wiki.gg hrefs from here and start bfs
    # h1 id="firstHeading" (page title) div class="mw-content-ltr mw-parser-output flash-anchored" (body) <--- for other pages
    soup = bs4.BeautifulSoup(main_site.text, "html.parser")
    body = soup.find("div", {"id": "main-section"})
    hyperlinks = [a for a in body.find_all("a", attrs={'href': re.compile(r'^/wiki')}) if not a.find("img")]
    sleep(10*random())
    for link in hyperlinks:
        print(link.text, ": ", link.get("href"))
        get_url(URL + link.get("href"), session)
        sleep(10*random())
    print("yeah")
    sleep(5)
    all_pages = bfs(hyperlinks, session, 1)

