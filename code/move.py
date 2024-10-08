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
        self.boosts = self.init_boosts(data["battleStageMod"])
        self.status = data["moveStatus"]

    @staticmethod
    def init_boosts(data):
        if data:
            boosts = {"atk": 0, "deff": 0, "aspe": 0, "dspe": 0, "spd": 0, "acc": 0, "eva": 0}
            stats_trad = {"ATK_STAGE": "atk",
                          "DFE_STAGE": "deff",
                          "ATS_STAGE": "aspe",
                          "DFS_STAGE": "dspe",
                          "SPD_STAGE": "spd",
                          "ACC_STAGE": "acc",
                          "EVA_STAGE": "eva"}
            for mod in data:
                for stat in stats_trad:
                    if stat in mod["battleStage"]:
                        boosts[stats_trad[stat]] = mod["modificator"]
            return boosts
        return None
