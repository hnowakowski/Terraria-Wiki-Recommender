import bs4
import requests
import re
from time import sleep
from random import random
from random import uniform
import cloudscraper
import pandas as pd

# scraping guidelines
# https://terraria.wiki.gg/robots.txt

# can be some template pages if they ever pop up
URL_BLACKLIST = []


URL = "https://terraria.wiki.gg"

def get_url(url, scraper):
    res = scraper.get(url)
    if res.status_code != 200:
        print(f"WARNING! Get request returned code other than 200: {res.status_code}")
    if res.status_code == 429:
        print("Returned 429, retrying in 15 seconds, but tbh you've already prob been blacklisted, you're cooked bro 💀💀💀")
        sleep(15)
        res = scraper.get(url)
        if res.status_code == 429:
            raise ConnectionRefusedError("try in a few hours or on a different ip lol")
    if res.status_code == 200:
        print(f"Url fetched successfully: {url}")
    return res.text

def bfs(initial_links, scraper, df, iterations):
    queue = initial_links
    visited = set(initial_links[:])
    while iterations and queue:
        sleep(uniform(2, 4) + 1) # robots.txt says 1 sec cooldown is fine but i still sometimes got blocked by cloudflare
        curr_link = queue.pop(0)
        curr = get_url(URL + curr_link, scraper)
        soup = bs4.BeautifulSoup(curr, "html.parser")
        title = soup.find("h1", {"id": "firstHeading"}).text
        body = soup.find("div", {"class": "mw-content-ltr mw-parser-output"})
        new_links = [a.get("href") for a in body.find_all("a", attrs={'href': re.compile(r'^/wiki')}) if not a.find("img")]
        df = pd.concat((df,
                         pd.DataFrame([[title, curr_link, body.text.strip().replace('\n', ' ').replace('  ', ' ')]],
                                       columns=["title", "link", "body"])), ignore_index=True)
        for link in new_links:
            if link not in visited:
                visited.add(link)
                queue.append(link)
        iterations -= 1
    return df



def scrape():
    df = pd.DataFrame(columns=["title", "link", "body"])
    scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0',})
    main_site = get_url(URL, scraper)
    # id="main-section" <-- extract all wiki.gg hrefs from here and start bfs
    # h1 id="firstHeading" (page title) div class="mw-content-ltr mw-parser-output" (body) <--- for other pages
    soup = bs4.BeautifulSoup(main_site, "html.parser")
    body = soup.find("div", {"id": "main-section"})
    links = [a.get("href") for a in body.find_all("a", attrs={'href': re.compile(r'^/wiki')}) if not a.find("img")]
    df = bfs(links, scraper, df, 2000)
    print(df)
    df.to_csv("raw_text.csv")

