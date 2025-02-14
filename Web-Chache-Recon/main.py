from utils.input_handler import handle_input
from utils.crawler import crawl
from utils.cache_fetcher import fetch_from_cache
from utils.analyzer import analyze_data
from utils.logger import setup_logger

# Initialize the logger
logger = setup_logger()

def main():
    try:
        # Step 1: Get Input from the User
        logger.info("Starting the WebCacheRecon tool.")
        target_url = handle_input()

        if not target_url:
            logger.error("No valid input received. Exiting...")
            return

        # Step 2: Crawl the Target URL
        logger.info(f"Initiating crawling for: {target_url}")
        crawled_data = crawl(target_url)

        if crawled_data is None:
            logger.error("Crawling failed. Exiting...")
            return

        # Step 3: Fetch Cached Data
        logger.info(f"Fetching cached data for: {target_url}")
        cached_data = fetch_from_cache(target_url)

        if cached_data is None:
            logger.warning(f"No cache found for {target_url}. Proceeding without cache.")

        # Step 4: Analyze the Data
        logger.info("Starting analysis on the crawled and cached data.")
        analysis_result = analyze_data(cached_data if cached_data else crawled_data)

        if analysis_result:
            logger.info("Analysis completed successfully.")
            print("Analysis Result:")
            print(analysis_result)
        else:
            logger.warning("Analysis could not be completed.")

    except Exception as e:
        logger.critical(f"Unexpected error in main workflow: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
