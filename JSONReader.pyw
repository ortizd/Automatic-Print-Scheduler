import json
class JsonReader:
        
    # Create read and write functios to use from the other files
    def read_json(self):
        with open("config.json", "r") as file:
            data = json.load(file)
        return data

    def write_json(self, data):
        with open("config.json", "w") as file:
            data= json.dump(data, file, indent=4)
