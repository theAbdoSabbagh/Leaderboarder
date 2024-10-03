import json

class Jsonifier:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.data = None

        self.load_data(self.file_name)
    
    def load_data(self, file_name: str):
        with open(file_name, "r+") as file:
            self.data = json.load(file)

    def save_data(self):
        with open(self.file_name, "w+") as file:
            json.dump(self.data, file, indent = 4)
