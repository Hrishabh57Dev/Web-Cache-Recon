# Web Cache Recon

## Overview
Web Cache Recon is a command-line tool that extracts sensitive information from cached web pages. It retrieves cached versions of target URLs from sources like **Google Cache** and **Wayback Machine**, then scans for exposed credentials, API keys, and other sensitive data.

## Features
- 🔍 Fetch cached versions of web pages from **Google Cache** and **Wayback Machine**.
- 🔑 Extract **sensitive information** such as API keys, emails, and passwords using regex.
- ⚡ Supports **automated reconnaissance** for penetration testing and bug bounty hunting.
- 🖥️ **CLI-based tool** for easy integration into security workflows.

## Use Cases
- **🕵️ Bug Bounty Hunting** – Discover sensitive data left in cached web pages.
- **🔓 Penetration Testing** – Identify exposed credentials and security misconfigurations.
- **📝 Digital Forensics** – Retrieve historical data from deleted or modified pages.
- **🌍 Threat Intelligence** – Monitor cached versions of websites for potential data leaks.

## Steps to install
 Clone the repository:
   ```bash
   git clone https://github.com/Hrishabh57Dev/Web-Cache-Recon.git
   cd web-cache-recon
   pip install -r requirements.txt
```


## External Tools Required
- **Katana:** Used for efficient crawling of web pages.
  - Install via: `go install github.com/projectdiscovery/katana/cmd/katana@latest`
  - Ensure it is in your system's PATH.

