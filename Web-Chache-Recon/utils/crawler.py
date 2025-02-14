import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time
from utils.logger import setup_logger
import subprocess

def run_katana(target_url):
    """
    Runs Katana to crawl the target URL and returns the result as a string.
    """
    try:
        # Command to run Katana
        command = ["katana", "-u", target_url, "-silent", "-o", "katana_output.txt"]
        subprocess.run(command, check=True)

        # Read and return the output
        with open("katana_output.txt", "r") as f:
            result = f.read()
        return result
    except Exception as e:
        print(f"Error running Katana: {e}")
        return None

# Initialize the logger
logger = setup_logger()

def crawl(url):
    try:
        # Simulated crawling logic
        logger.info(f"Starting crawl for URL: {url}")
        # Code that may fail
        if not url.startswith("http"):
            raise ValueError(f"Invalid URL: {url}")
        # Example of a successful crawl
        return f"Crawled data from {url}"
    except Exception as e:
        logger.error(f"Error while crawling {url}: {str(e)}")
        return None


def fetch_wayback_urls(domain):
    """
    Fetch URLs for a domain from the Wayback Machine.
    """
    print(f"Fetching cached URLs from Wayback Machine for domain: {domain}")
    wayback_api_url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&filter=statuscode:200"
    try:
        response = requests.get(wayback_api_url, timeout=10)
        response.raise_for_status()
        wayback_urls = [entry[0] for entry in response.json()[1:]]  # Skip the header row
        return wayback_urls
    except Exception as e:
        print(f"Error fetching URLs from Wayback Machine: {e}")
        return []

def fetch_google_cache(url):
    """
    Fetch a cached version of a URL from Google Cache.
    """
    print(f"Fetching Google Cache for URL: {url}")
    google_cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
    try:
        response = requests.get(google_cache_url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching Google Cache for {url}: {e}")
        return None

def fetch_content(url):
    """
    Fetch the HTML content of a given URL.
    """
    print(f"Fetching content for URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching content for {url}: {e}")
        return None

def crawl_and_fetch(urls, source="wayback", max_threads=5):
    """
    Crawl a list of URLs and fetch their cached content.
    """
    print(f"Starting crawl for source: {source}")
    results = []

    def worker(url):
        if source == "wayback":
            return fetch_content(url)
        elif source == "google":
            return fetch_google_cache(url)
        return None

    with ThreadPoolExecutor(max_threads) as executor:
        for result in executor.map(worker, urls):
            if result:
                results.append(result)

    print(f"Crawling complete. Fetched {len(results)} pages.")
    return results

def extract_links(html, base_url):
    """
    Extract all links from the HTML content.
    """
    print(f"Extracting links from base URL: {base_url}")
    try:
        soup = BeautifulSoup(html, "html.parser")
        links = [urljoin(base_url, tag.get("href")) for tag in soup.find_all("a", href=True)]
        return list(set(links))  # Remove duplicates
    except Exception as e:
        print(f"Error extracting links: {e}")
        return []

if __name__ == "__main__":
    # Test the crawler functions
    domain = "example.com"
    print("Testing Wayback Machine URL fetch...")
    wayback_urls = fetch_wayback_urls(domain)
    print(f"Wayback URLs: {wayback_urls[:5]}")  # Show only the first 5 URLs for brevity

    if wayback_urls:
        print("Testing crawl and fetch for Wayback URLs...")
        content = crawl_and_fetch(wayback_urls[:5], source="wayback")
        print(f"Fetched {len(content)} pages.")

    test_url = "http://example.com"
    print("Testing link extraction...")
    html = fetch_content(test_url)
    if html:
        links = extract_links(html, test_url)
        print(f"Extracted links: {links[:5]}")  # Show only the first 5 links for brevity
