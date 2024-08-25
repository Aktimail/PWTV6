import math
import random
import json

from data import DATA
from move import Move
from type import Type


class Pokemon:
    def __init__(self, name, level, mod=None):
        data = json.load(open(f"../assets/json/pokemons/{name.lower()}.json"))
        self.forms = data["forms"]

        self.klass = data["klass"]
        self.id = data["id"]
        self.name = data["dbSymbol"]
        self.height = self.forms[0]["height"]
        self.weight = self.forms[0]["weight"]
        self.shiny = True if random.random() <= 1 / 8192 else False

        self.level = level

        self.gender = self.get_gender()
        self.type = self.get_type()
        self.ability = random.choice(self.forms[0]["abilities"])
        self.item = None

        self.movepool = self.forms[0]["moveSet"]
        self.moveset = self.init_moveset()

        self.base_stats = {"hp": self.forms[0]["baseHp"],
                           "atk": self.forms[0]["baseAtk"],
                           "deff": self.forms[0]["baseDfe"],
                           "aspe": self.forms[0]["baseAts"],
                           "dspe": self.forms[0]["baseDfs"],
                           "spd": self.forms[0]["baseSpd"]
                           }

        self.ivs = {"hp": random.randint(0, 31),
                    "atk": random.randint(0, 31),
                    "deff": random.randint(0, 31),
                    "aspe": random.randint(0, 31),
                    "dspe": random.randint(0, 31),
                    "spd": random.randint(0, 31)
                    }

        self.evs = {"hp": self.forms[0]["evHp"],
                    "atk": self.forms[0]["evAtk"],
                    "deff": self.forms[0]["evDfe"],
                    "aspe": self.forms[0]["evAts"],
                    "dspe": self.forms[0]["evDfs"],
                    "spd": self.forms[0]["evSpd"]
                    }

        self.nature = random.choice(tuple(DATA.ALL_NATURES.values()))

        self.hp = self.update_stat("hp")
        self.max_hp = self.hp
        self.atk = self.update_stat("atk")
        self.deff = self.update_stat("deff")
        self.aspe = self.update_stat("aspe")
        self.dspe = self.update_stat("dspe")
        self.spd = self.update_stat("spd")

        self.boosts = {"atk": 0, "deff": 0, "aspe": 0, "dspe": 0, "spd": 0}
        self.status = {"main": None, "sec": None}

        self.exp_type = self.forms[0]["experienceType"]
        self.exp = 0
        self.remaining_exp = self.remaining_exp_update()

        self.init_mods(mod)

        self.ko = False

        self.spritesheet = f"../assets/battle/pkmn_sprite_5g/{self.id}.png"
        self.back_spritesheet = f"../assets/battle/pkmn_sprite_5g/back/{self.id}.png"
        if self.shiny:
            self.spritesheet = f"../assets/battle/pkmn_sprite_5g/shiny/{self.id}.png"
            self.back_spritesheet = f"../assets/battle/pkmn_sprite_5g/back/shiny/{self.id}.png"
        if self.gender == "female":
            pass

        self.front_offset_y = self.forms[0]["frontOffsetY"]

        self.comments = []
        self.damages_received = 0

    def get_gender(self):
        if self.forms[0]["femaleRate"] == -1:
            return "genderless"
        return "female" if random.randint(1, 100) <= self.forms[0]["femaleRate"] else "male"

    def get_type(self):
        if self.forms[0]["type2"] == "__undef__":
            return [Type(self.forms[0]["type1"])]
        return [Type(self.forms[0]["type1"]),
                Type(self.forms[0]["type2"])]

    def init_mods(self, mod):
        if mod:
            if "gender" in mod:
                self.gender = mod[self.name]["gender"]

            if "ivs" in mod:
                for stat in mod["ivs"]:
                    self.ivs[stat] = mod["ivs"][stat]

            if "evs" in mod:
                for stat in mod["evs"]:
                    self.evs[stat] = mod["evs"][stat]

            if "nature" in mod:
                self.nature = mod["nature"]

            if "moveset" in mod:
                self.moveset.clear()
                for move in mod["moveset"]:
                    self.moveset.append(Move(move))

            if "ability" in mod:
                self.ability = mod["ability"]

            if "item" in mod:
                self.item = mod["item"]

            if "shiny" in mod:
                self.shiny = mod["shiny"]

            if "hp" in mod:
                self.hp = mod["hp"]

            if "max_hp" in mod:
                self.max_hp = mod["max_hp"]

    def init_moveset(self):
        moveset = []
        for move in self.movepool:
            if move["klass"] == "LevelLearnableMove":
                if move["level"] <= self.level:
                    moveset.append(Move(move["move"]))
                    if len(moveset) > 4:
                        moveset.remove(random.choice(moveset))
        return moveset

    def update_hp(self):
        if self.damages_received:
            self.damages_received -= 1
            self.hp -= 1
            self.check_hp()

    def update_stat(self, stat):
        if stat == "hp":
            return math.floor(((self.ivs[stat] + 2 * self.base_stats[stat] + math.floor(self.evs[stat] / 4)) *
                               self.level / 100) + self.level + 10)
        return math.floor((((self.ivs[stat] + 2 * self.base_stats[stat] + math.floor(self.evs[stat] / 4)) *
                            self.level / 100) + 5) * self.nature[stat])

    def check_hp(self):
        if self.hp <= 0:
            self.hp = 0
            self.ko = True
            self.comments.append(str(self.name + " is ko !"))

    def remaining_exp_update(self):
        if self.level == 100:
            return 0
        if self.exp_type == 0:
            return self.level ** 3
        elif self.exp_type == 1:
            return math.floor((4 * (self.level ** 3)) / 5)
        elif self.exp_type == 2:
            return 5 * (self.level ** 3) / 4
        elif self.exp_type == 3:
            return math.floor(((6 / 5) * (self.level ** 3)) - (15 * (self.level ** 2)) + (100 * self.level) - 140)
        elif self.exp_type == 4:
            if self.level <= 50:
                return math.floor((self.level ** 3) * (100 - self.level) / 50)
            elif self.level <= 68:
                return math.floor((self.level ** 3) * (150 - self.level) / 100)
            elif self.level <= 98:
                return math.floor((self.level ** 3) * math.floor((1911 - 10 * self.level) / 3) / 500)
            elif self.level <= 100:
                return math.floor((self.level ** 3) * (160 - self.level) / 100)

    def can_attack(self, move: Move, target):
        if self.ko or move.pp <= 0:
            return False

        if self.status["main"] == "sleep" and move.name != "Sleep Talk":
            self.comments.append(str(self.name + " is fast asleep !"))
            return False

        if self.status["main"] == "freeze":
            self.comments.append(str(self.name + " is frozen solid !"))
            return False

        if self.status["sec"] == "flinch":
            self.comments.append(str(self.name + " flinched and couldn't move !"))
            return False

        if self.status["main"] == "paralysis":
            self.comments.append(str(self.name + " is paralyzed !"))
            if random.randint(0, 100) <= 25:
                self.comments.append("It can't move !")
                return False

        if self.status["sec"] == "confusion":
            self.comments.append(str(self.name + " is confused !"))
            if random.randint(0, 100) <= 33:
                self.comments.append("It hurt itself in its confusion !")
                self.hp = int(self.hp - (((((self.level * 2 / 5) + 2) * 40 * self.atk / 50) / self.deff) + 2) *
                              ((random.randint(217, 255) * 100) / 255) / 100)
                self.check_hp()
                return False

        if self.status["sec"] == "attract":
            self.comments.append(str(self.name + " is in love with " + target.name + " !"))
            if random.randint(0, 100) <= 50:
                self.comments.append(str(self.name + " is immobilized by love !"))
                return False
        return True

    def calcul_damages(self, move: Move, target):
        if move.power:
            # power
            hh = 1
            it = 1
            chg = 1
            ms = 1
            ws = 1
            ua = 1
            fa = 1
            power = hh * move.power * it * chg * ms * ws * ua * fa
            # atk
            move_category = self.atk
            if move.category == "special":
                move_category = self.aspe
            am = 1
            im = 1
            atk = move_category * am * im
            # deff
            target_deff = target.deff
            if move.category == "special":
                target_deff = target.dspe
            sx = 1
            mod = 1
            deff = target_deff * sx * mod
            # mod 1
            brn = 1
            rl = 1
            tvt = 1  # 2v2
            sr = 1
            ff = 1
            mod1 = brn * rl * tvt * sr * ff
            # mod 2
            mod2 = 1
            # critical hit
            crit = 1
            if random.uniform(0, 100) <= 6.25:
                crit = 2
                self.comments.append("A critical hit !")
            # random
            r = (random.randint(217, 255) * 100) / 255
            # stab
            stab = 1
            for t in self.type:
                if move.type.name == t.name:
                    stab = 1.5
            # types
            typeA, typeB = 1, 1
            if target.type[0].name in move.type.immunes:
                typeA = 0
            elif target.type[0].name in move.type.weaknesses:
                typeA = 0.5
            elif target.type[0].name in move.type.strengths:
                typeA = 2
            if len(target.type) > 1:
                if target.type[1].name in move.type.immunes:
                    typeB = 0
                elif target.type[1].name in move.type.weaknesses:
                    typeB = 0.5
                elif target.type[1].name in move.type.strengths:
                    typeB = 2

            if typeA == 0 or typeB == 0:
                self.comments.append(str("It doesn't affect " + target.name))
            elif typeA + typeB < 2:
                self.comments.append("It's not very effective...")
            elif typeA + typeB > 2.5:
                self.comments.append("It's super effective !")
            # mod 3
            srf = 1
            eb = 1
            tl = 1
            trb = 1
            mod3 = srf * eb * tl * trb
            # calcul
            dmgs = int(self.level * 2 / 5)
            dmgs = int(dmgs) + 2
            dmgs = int(dmgs) * power * atk / 50
            dmgs = int(dmgs) / deff
            dmgs = int(dmgs) * mod1
            dmgs = int(dmgs) + 2
            dmgs = int(dmgs) * crit * mod2 * r / 100
            dmgs = int(int(dmgs) * stab * typeA * typeB * mod3)
            return dmgs
        return 0

    def attack(self, move: Move, target):
        if self.can_attack(move, target):
            self.comments.append(str(self.name + " use " + move.name))
            move.pp -= 1
            if not move.accuracy or random.randint(0, 100) <= move.accuracy:
                if move.category == "status":
                    pass
                else:
                    dmgs = self.calcul_damages(move, target)
                    target.damages_received = dmgs
                    target.check_hp()
            else:
                self.comments.append("But it failed !")
        return

    def show_info(self):
        print(self.name, end=""), print(" | " + str(self.status["main"]) if not self.status["main"] is None else "")
        print(str(self.hp) + "/" + str(self.max_hp))
        print("===============")
        for t in self.type:
            print(t)
        print()
        print("N°" + str(self.id), "| Gender :", self.gender, "| Lvl", self.level)
        print("Ability :", self.ability, "| Item :", self.item)
        print("===============")
        print("Stats :")
        stats_name = ["atk", "deff", "aspe", "dspe", "spd"]
        stats = [self.atk, self.deff, self.aspe, self.dspe, self.spd]
        for sn, s in zip(stats_name, stats):
            print(sn, ":", s, "")
        print("===============")
        print("Moves :")
        for m in self.moveset:
            print(m.name, str(m.pp) + "/" + str(m.max_pp))
