import json


class Move:
    def __init__(self, name):
        data = json.load(open(f"../assets/json/moves/{name}.json"))

        self.klass = data["klass"]
        self.id = data["id"]
        self.name = data["dbSymbol"]
        self.type = data["type"]

        self.power = data["power"]
        self.accuracy = data["accuracy"]
        self.pp = data["pp"]
        self.max_pp = self.pp
        self.category = data["category"]

        self.critical_rate = data["movecriticalRate"]
        self.priority = data["priority"]
        self.feature = {
            "direct": data["isDirect"],
            "charge": data["isCharge"],
            "recharge": data["isRecharge"],
            "blocable": data["isBlocable"],
            "snatchable": data["isSnatchable"],
            "mirror move": data["isMirrorMove"],
            "punch": data["isPunch"],
            "gravity": data["isGravity"],
            "magic coat affected": data["isMagicCoatAffected"],
            "unfreeze": data["isUnfreeze"],
            "sound attack": data["isSoundAttack"],
            "distance": data["isDistance"],
            "heal": data["isHeal"],
            "authentic": data["isAuthentic"],
            "bite": data["isBite"],
            "pulse": data["isPulse"],
            "ballistics": data["isBallistics"],
            "mental": data["isMental"],
            "non sky battle": data["isNonSkyBattle"],
            "dance": data["isDance"],
            "king rock utility": data["isKingRockUtility"],
            "powder": data["isPowder"],
        }
        self.effect_chance = data["effectChance"]
        self.target = data["battleEngineAimedTarget"]
        self.stat_mod = data["battleStageMod"]
        self.status = data["moveStatus"]
