import json


class Item:
    def __init__(self, name):
        data = json.load(open(f"../assets/json/items/{name}.json"))
        self.id = data["id"]
        self.name = data["dbSymbol"]
        self.icon = data["icon"]
        self.price = data["price"]
        self.socket = data["socket"]
        self.position = data["position"]
        self.battle_usable = data["isBattleUsable"]
        self.map_usable = data["isMapUsable"]
        self.limited = data["isLimited"]
        self.holdable = data["isHoldable"]
        self.fling_power = data["flingPower"]
