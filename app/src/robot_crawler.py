import os
import requests
from bs4 import BeautifulSoup

USER_AGENT = "USER_AGENT"

def get_page(url, headers):
    try:
        res = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
        return None
    return res.text

def scrape_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text

def normalize(s):
    return s.strip()

def main():
    headers = {}
    current = os.path.dirname(__file__)
    if USER_AGENT in os.environ:
        headers = {"User-Agent": os.environ[USER_AGENT]}
    urls = []
    with open(current + '/urls.txt') as f:
        urls = [url.rstrip() for url in f]

    count = 0
    for url in urls:
        html = get_page(url, headers)
        if html:
            text = scrape_page(html)
            text = normalize(text)
            file_name = url.split("/")[-1]
            if not file_name:
                file_name = str(count)
                count += 1
            output_path = current + "/output/" + file_name + ".txt"

            # TODO: 同じファイル名が出力されると消える
            with open(output_path, "w") as f:
                f.write(text)

if __name__ == '__main__':
    main()
