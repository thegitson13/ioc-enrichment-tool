from pathlib import Path
import logging
import os
from detector import Detector
from validators import Validators
from reporter import Reporter

PATH_TO_DATA = Path(__file__).parent /"data/sample_iocs.txt"
PATH_TO_REPORT = Path(__file__).parent /"report.json"
url = 'https://api.abuseipdb.com/api/v2/check'
api_key = os.getenv("ABUSEIPDB_API_KEY")
if not api_key:
    logging.error("ABUSEIPDB_API_KEY environment variable is not set.")
    exit(1)

def load_file():
    data = []

    if not PATH_TO_DATA.exists():
        logging.error(f"Error: The file {PATH_TO_DATA} does not exists")
    else:
        with open(PATH_TO_DATA, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                data.append(line.strip())

    return data

def my_choice():
    print("Would you like to display the report in the console or save it to a file?    ")
    while True:
        choice = input("Enter 'console' or 'file': ").strip().lower()
        if choice in ["console", "file"]:
            return choice
        else:
            print("Invalid input. Please enter 'console' or 'file'.")

if __name__ == "__main__":
    data = load_file()
    detector = Detector(data)
    result, unknown = detector.data_detector()
    validators = Validators(result)
    local_validation = validators.validate_ip()
    api_validation = validators.api_validator(local_validation, api_key, url)
    combined_data = validators.data_combiner(api_validation, result, unknown)
    decision = my_choice()
    if decision == "console":
        print(combined_data)
    elif decision == "file":
        reporter = Reporter(combined_data, PATH_TO_REPORT)
        reporter.save_to_file()
        print(f"Report saved to {PATH_TO_REPORT }")
    