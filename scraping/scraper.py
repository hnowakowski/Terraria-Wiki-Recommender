import bs4
import requests

# can be some regex later to avoid template pages if they ever pop up
URL_BLACKLIST = [
]

def getHtml(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"WARNING! Get request returned code other than 200: {res.status_code}")
    return res.text

def scrape():
    main_site = getHtml("https://terraria.wiki.gg/")
    # id="main-section" <-- extract all wiki.gg hrefs from here and start bfs
    # h1 id="firstHeading" (page title) div class="mw-content-ltr mw-parser-output flash-anchored" (body) <--- for other pages
    soup = bs4.BeautifulSoup(main_site, "html.parser")
    body = soup.find("div", {"id": "main-section"})
    hyperlinks = [a for a in body.find_all("a") if not a.find("img")]
    for hyper in hyperlinks:
        print(hyper.text, ": ", hyper.get("href"))
