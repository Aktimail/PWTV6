import json


class Type:
    def __init__(self, name):
        data = json.load(open("../assets/json/types.json"))
        for i in range(len(data)):
            if data[i]["name"] == name:
                self.name = [data[i]["name"]][0]
                self.weaknesses = [data[i]["weaknesses"]]
                self.strengths = [data[i]["strengths"]]
                self.immunes = [data[i]["immunes"]]
