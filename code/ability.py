import json


class Ability:
    def __init__(self, name):
        data = json.load(open(f"../assets/json/abilities/{name}.json"))
        self.name = data["dbSymbol"]
        self.id = data["id"]
        self.txt_id = data["textId"]
