import json
from type import Type


class Move:
    def __init__(self, name):
        data = json.load(open(f"../assets/json/moves/{name}.json"))

        self.klass = data["klass"]
        self.id = data["id"]
        self.name = data["dbSymbol"]
        self.type = Type(data["type"])

        self.power = data["power"]
        self.accuracy = data["accuracy"]
        self.pp = data["pp"]
        self.max_pp = self.pp
        self.category = data["category"]

        self.critical_rate = data["movecriticalRate"]
        self.battle_engine_method = data["battleEngineMethod"]
        self.priority = data["priority"]
        self.feature = {
            "direct": data["isDirect"],
            "charge": data["isCharge"],
            "recharge": data["isRecharge"],
            "blocable": data["isBlocable"],
            "snatchable": data["isSnatchable"],
            "mirror_move": data["isMirrorMove"],
            "punch": data["isPunch"],
            "gravity": data["isGravity"],
            "magic_coat_affected": data["isMagicCoatAffected"],
            "unfreeze": data["isUnfreeze"],
            "sound_attack": data["isSoundAttack"],
            "distance": data["isDistance"],
            "heal": data["isHeal"],
            "authentic": data["isAuthentic"],
            "bite": data["isBite"],
            "pulse": data["isPulse"],
            "ballistics": data["isBallistics"],
            "mental": data["isMental"],
            "non_sky_battle": data["isNonSkyBattle"],
            "dance": data["isDance"],
            "king_rock_utility": data["isKingRockUtility"],
            "powder": data["isPowder"],
        }
        self.effect_chance = data["effectChance"]
        self.target = data["battleEngineAimedTarget"]
        self.stat_mod = data["battleStageMod"]
        self.status = data["moveStatus"]
