import json
import logging

class Reporter:
    def __init__(self, data, path):
        self.data = data
        self.path = path

    def save_to_file(self):
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4)
        except IOError as e:
            logging.error(f"Error saving report to {self.path}: {e}")