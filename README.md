# IOC Enrichment Tool

A Python-based IOC (Indicator of Compromise) enrichment tool designed to detect, validate, and enrich common indicators used in cybersecurity investigations.

The tool reads indicators from a text file, automatically identifies their type, performs local validation, enriches public IP addresses using the AbuseIPDB API, and generates a report.

## Features

- Reads multiple IOCs from a text file
- Automatically detects IOC types:
  - IPv4
  - IPv6
  - Domains
  - MD5 hashes
  - SHA1 hashes
  - SHA256 hashes
- Identifies unknown or invalid input
- Performs local IP address validation
- Detects private, loopback, and multicast IP addresses
- Skips non-public IP addresses from external enrichment
- Enriches public IP addresses using AbuseIPDB
- Retrieves information such as:
  - Abuse confidence score
  - Country code
  - ISP
  - Domain
  - Number of reports
  - Tor status
- Displays results in the terminal
- Supports exporting results to a JSON report

## Project Structure

```text
ioc-enrichment-tool/
├── data/
│   └── sample_iocs.txt
├── detector.py
├── ioc_enricher.py
├── reporter.py
├── validators.py
├── requirements.txt
├── README.md
└── .gitignore
