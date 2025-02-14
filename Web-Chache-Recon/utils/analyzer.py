import re
from utils.logger import setup_logger

# Initialize the logger
logger = setup_logger()

def analyze_data(data):
    try:
        # Simulated analysis logic
        logger.info("Starting analysis on fetched data.")
        if not data:
            raise ValueError("No data provided for analysis.")
        # Example of a successful analysis
        return f"Analysis complete: {len(data)} characters processed."
    except ValueError as e:
        logger.error(f"Data analysis error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {str(e)}")
        return None


def analyze_content(content, regex_patterns):
    """
    Analyze the cached content for sensitive data or patterns.
    
    :param content: The HTML/text content to analyze.
    :param regex_patterns: A list of regex patterns to search for.
    :return: A dictionary with matches for each pattern.
    """
    analysis_results = {}
    print("Starting analysis of content...")
    for pattern_name, pattern in regex_patterns.items():
        print(f"Analyzing pattern: {pattern_name}")
        matches = re.findall(pattern, content, re.IGNORECASE)
        analysis_results[pattern_name] = matches
    return analysis_results


def predefined_patterns():
    """
    Define a set of predefined regex patterns for common sensitive data.
    
    :return: A dictionary of pattern names and their corresponding regex.
    """
    return {
        "API Keys": r"(?:api[_\-]?key|access[_\-]?token)[\s=:'\"`]{0,5}([a-zA-Z0-9\-_]{16,})",
        "Email Addresses": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "URLs": r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        "Passwords": r"(?:password|pwd|pass)[\s=:'\"`]{0,5}([a-zA-Z0-9@#$%^&*()-_+]{8,})",
        "AWS Keys": r"AKIA[0-9A-Z]{16}",
        "Private Keys": r"-----BEGIN PRIVATE KEY-----[\s\S]*?-----END PRIVATE KEY-----",
    }


def analyze_cached_data(cache_results):
    """
    Analyze cached content from different sources for sensitive data.
    
    :param cache_results: Dictionary containing cached HTML/text content from various sources.
    :return: Analysis results for each source.
    """
    patterns = predefined_patterns()
    all_analysis_results = {}
    
    for source, content in cache_results.items():
        print(f"Analyzing content from source: {source}")
        results = analyze_content(content, patterns)
        all_analysis_results[source] = results
    
    return all_analysis_results


if __name__ == "__main__":
    # Example usage
    example_cache_results = {
        "wayback": "<html>API Key: abc123XYZ789abcd1234<br>Email: example@domain.com</html>",
        "google": "<html>Password: MySecretPass!@#<br>AWS Key: AKIA1234567890ABCD</html>",
    }

    print("Analyzing example cached data...")
    analysis_results = analyze_cached_data(example_cache_results)

    # Print analysis results
    for source, results in analysis_results.items():
        print(f"\nAnalysis Results for {source}:")
        for pattern_name, matches in results.items():
            print(f"  {pattern_name}: {matches}")
