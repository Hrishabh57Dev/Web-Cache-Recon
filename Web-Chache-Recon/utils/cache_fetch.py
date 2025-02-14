import requests
from utils.logger import setup_logger

# Initialize the logger
logger = setup_logger()

def fetch_from_cache(url):
    try:
        # Simulated cache fetching logic
        logger.info(f"Fetching cache for URL: {url}")
        # Simulated error
        if "404" in url:
            raise FileNotFoundError(f"No cache found for {url}")
        # Example of successful fetch
        return f"Cached data for {url}"
    except FileNotFoundError as e:
        logger.error(f"Cache error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while fetching cache: {str(e)}")
        return None


def fetch_wayback_cache(url):
    """
    Fetch the cached version of a URL from the Wayback Machine.
    """
    print(f"Fetching Wayback Machine cache for URL: {url}")
    wayback_cache_url = f"http://web.archive.org/web/{url}"
    try:
        response = requests.get(wayback_cache_url, timeout=10)
        response.raise_for_status()
        return response.text  # Return the HTML content
    except Exception as e:
        print(f"Error fetching Wayback Machine cache for {url}: {e}")
        return None


def fetch_google_cache(url):
    """
    Fetch the cached version of a URL from Google Cache.
    """
    print(f"Fetching Google Cache for URL: {url}")
    google_cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
    try:
        response = requests.get(google_cache_url, timeout=10)
        response.raise_for_status()
        return response.text  # Return the HTML content
    except Exception as e:
        print(f"Error fetching Google Cache for {url}: {e}")
        return None


def fetch_cache(url, sources=None):
    """
    Fetch the cached version of a URL from the specified sources.
    
    :param url: The URL to fetch the cache for.
    :param sources: List of sources to fetch the cache from. Options: 'wayback', 'google'.
    :return: Dictionary containing cached HTML from the sources.
    """
    if sources is None:
        sources = ["wayback", "google"]

    cache_results = {}
    if "wayback" in sources:
        print(f"Attempting to fetch Wayback cache for: {url}")
        wayback_content = fetch_wayback_cache(url)
        if wayback_content:
            cache_results["wayback"] = wayback_content

    if "google" in sources:
        print(f"Attempting to fetch Google cache for: {url}")
        google_content = fetch_google_cache(url)
        if google_content:
            cache_results["google"] = google_content

    return cache_results


if __name__ == "__main__":
    # Test the cache fetcher with a sample URL
    test_url = "http://example.com"
    print(f"Fetching cached versions for: {test_url}")
    
    # Fetch cached versions from both Wayback Machine and Google Cache
    results = fetch_cache(test_url, sources=["wayback", "google"])
    
    # Display results
    for source, content in results.items():
        print(f"Cache fetched from {source}: {len(content)} characters")
