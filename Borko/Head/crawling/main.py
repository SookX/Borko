import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urlparse

def fetch_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve the page: {url} (Status code: {response.status_code})")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_links(page_content, base_url):
    soup = BeautifulSoup(page_content, 'lxml')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('http'):
            links.add(href)
        else:
            links.add(requests.compat.urljoin(base_url, href))
    return links

def is_subdomain(url, main_domain):
    parsed_url = urlparse(url).netloc
    return parsed_url.endswith(main_domain)

def crawl_website(start_url, main_domain, max_pages=50):
    crawled_urls = set()
    found_urls = set()
    to_crawl = [start_url]
    while to_crawl and len(crawled_urls) < max_pages:
        current_url = to_crawl.pop()
        print(f"Crawling: {current_url}")
        page_content = fetch_page(current_url)
        if page_content:
            crawled_urls.add(current_url)
            with open("crawled_urls.txt", "a", encoding="utf-8") as file:
                file.write(current_url + "\n")
                file.flush()
            new_links = extract_links(page_content, current_url)
            unique_new_links = {link for link in new_links if is_subdomain(link, main_domain) and link not in found_urls}
            found_urls.update(unique_new_links)
            print(f"Found {len(unique_new_links)} new unique subdomain links")
            with open("found_urls.txt", "a", encoding="utf-8") as file:
                for link in unique_new_links:
                    file.write(link + "\n")
                file.flush()
            to_crawl.extend([link for link in unique_new_links if link not in crawled_urls and link not in to_crawl])
        time.sleep(random.uniform(1, 3))
    return crawled_urls

if __name__ == "__main__":
    start_url = "https://www.framar.bg/"
    main_domain = "forum.framar.bg"  # Define the main domain to restrict crawling to subdomains
    max_pages = 500
    crawled_urls = crawl_website(start_url, main_domain, max_pages)
    print(f"\nCrawling complete. {len(crawled_urls)} pages crawled.")
