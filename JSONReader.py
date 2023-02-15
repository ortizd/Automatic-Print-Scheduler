import json
class JsonReader:
        
    
    def read_json(self):
        with open("permanent_file.json", "r") as file:
            data = json.load(file)
        return data

    def write_json(self, data):
        with open("permanent_file.json", "w") as file:
            data= json.dump(data, file, indent=4)
