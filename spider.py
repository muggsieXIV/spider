import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import datetime

class Spider:
    def __init__(self, url, keywords):
        self.url = url
        self.keywords = [keyword.lower() for keyword in keywords.split()]
        self.visited_urls = set()

    def is_valid_url(self, url):
        # Check if the URL is an HTTP or HTTPS link
        return urlparse(url).scheme in ('http', 'https')

    def spider_urls(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                a_tags = soup.find_all('a')
                for tag in a_tags:
                    href = tag.get("href")
                    if href and href != "" and self.is_valid_url(href):
                        url_join = urljoin(url, href)
                        if url_join.lower() not in self.visited_urls and all(keyword in url_join.lower() for keyword in self.keywords):
                            self.visited_urls.add(url_join.lower())
                            yield url_join  # Yield the URL for further processing
        except Exception as error:
            print(f"Request failed {url}, error: {error}")

    def start_spider(self):
        start_time = datetime.datetime.now()
        urls_to_visit = [self.url]
        while urls_to_visit:
            url = urls_to_visit.pop(0)
            new_urls = self.spider_urls(url)
            urls_to_visit.extend(new_urls)
        end_time = datetime.datetime.now()

        result = {
            "message": "Spider Process Completed",
            "URL": self.url,
            "Keywords": " ".join(self.keywords),
            "time_completed": end_time,
            "visited": len(self.visited_urls),
            "urls": self.visited_urls
        }

        return result

def main():
    url = input("Enter the URL you want to scrape: ")
    keywords = input("Enter the keywords (separated by spaces) to search for in the URL provided: ")

    spider = Spider(url, keywords)
    result = spider.start_spider()
    print(result)

if __name__ == "__main__":
    main()
