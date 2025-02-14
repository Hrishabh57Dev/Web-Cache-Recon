import argparse
import os
import re

def get_user_input():
    """
    Handles user input from the command line and validates it.
    Returns a dictionary of inputs for the tool.
    """
    parser = argparse.ArgumentParser(
        description="Web Cache Recon - A tool for analyzing cached web pages and identifying sensitive data."
    )

    # Add arguments for the tool
    parser.add_argument(
        "-u", "--url", 
        type=str, 
        help="Target URL to analyze (e.g., https://example.com)."
    )
    parser.add_argument(
        "-f", "--file", 
        type=str, 
        help="Path to a file containing multiple URLs to analyze."
    )
    parser.add_argument(
        "-s", "--source", 
        type=str, 
        choices=["wayback", "google", "custom"], 
        default="wayback", 
        help="Cache source to use (default: wayback)."
    )
    parser.add_argument(
        "-r", "--regex", 
        type=str, 
        help="Path to a custom regex file (optional)."
    )
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        choices=["json", "csv", "markdown"], 
        default="json", 
        help="Output format for the results (default: json)."
    )
    parser.add_argument(
        "-d", "--output-dir", 
        type=str, 
        default="./output", 
        help="Directory to save the results (default: ./output)."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Validate inputs
    if not args.url and not args.file:
        raise ValueError("You must provide a target URL (-u) or a file containing URLs (-f).")

    # Validate URL if provided
    if args.url and not is_valid_url(args.url):
        raise ValueError(f"The provided URL '{args.url}' is not valid. Please provide a valid URL.")

    # Validate file path if provided
    if args.file and not os.path.isfile(args.file):
        raise ValueError(f"The provided file '{args.file}' does not exist or is not accessible.")

    # Validate regex file if provided
    if args.regex and not os.path.isfile(args.regex):
        raise ValueError(f"The provided regex file '{args.regex}' does not exist or is not accessible.")

    # Create the output directory if it does not exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Load URLs from file if provided
    urls = []
    if args.file:
        with open(args.file, "r") as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
    else:
        urls = [args.url]

    # Load custom regex patterns if provided
    regex_patterns = None
    if args.regex:
        with open(args.regex, "r") as file:
            regex_patterns = [line.strip() for line in file.readlines() if line.strip()]

    # Return a structured input dictionary
    return {
        "urls": urls,
        "cache_source": args.source,
        "regex_patterns": regex_patterns,
        "output_format": args.output,
        "output_dir": args.output_dir,
    }

def is_valid_url(url):
    """
    Validates the provided URL.
    """
    regex = re.compile(
        r"^(https?:\/\/)?"  # HTTP or HTTPS
        r"([a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})+)"  # Domain name
        r"(:\d+)?(\/.*)?$"  # Optional port and path
    )
    return re.match(regex, url) is not None


if __name__ == "__main__":
    # For testing purposes
    try:
        user_input = get_user_input()
        print("Parsed User Input:")
        print(user_input)
    except Exception as e:
        print(f"Error: {e}")
