import math
import random
import json

from data import DATA
from move import Move
from type import Type
from item import Item
from ability import Ability


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
        self.ability = Ability(random.choice(self.forms[0]["abilities"]))
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

        self.init_mods(mod)

        self.hp = self.init_stats("hp")
        self.max_hp = self.hp
        self.atk = self.init_stats("atk")
        self.ig_atk = self.atk
        self.deff = self.init_stats("deff")
        self.ig_deff = self.deff
        self.aspe = self.init_stats("aspe")
        self.ig_aspe = self.aspe
        self.dspe = self.init_stats("dspe")
        self.ig_dspe = self.dspe
        self.spd = self.init_stats("spd")
        self.ig_spd = self.spd

        self.boosts = {"atk": 0, "deff": 0, "aspe": 0, "dspe": 0, "spd": 0, "acc": 0, "eva": 0}
        self.status = {"main": None, "sec": None}

        self.exp_type = self.forms[0]["experienceType"]
        self.exp = 0
        self.remaining_exp = self.exp_to_nxt_lvl()

        self.ko = False

        self.weather = None

        self.charge = False
        self.mud_sport = False
        self.water_sport = False
        self.reflect = False
        self.light_screen = False

        self.damages_received = 0

        self.spritesheet = f"../assets/battle/pkmn_sprite_5g/{self.id}.png"
        self.back_spritesheet = f"../assets/battle/pkmn_sprite_5g/back/{self.id}.png"
        if self.shiny:
            self.spritesheet = f"../assets/battle/pkmn_sprite_5g/shiny/{self.id}.png"
            self.back_spritesheet = f"../assets/battle/pkmn_sprite_5g/back/shiny/{self.id}.png"
        if self.gender == "female":
            pass

        self.front_offset_y = self.forms[0]["frontOffsetY"]

        self.comments = []

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
                self.nature = DATA.ALL_NATURES[mod["nature"]]

            if "moveset" in mod:
                for _ in range(len(mod["moveset"])):
                    self.moveset.remove(random.choice(self.moveset))
                for move in mod["moveset"]:
                    if move != "":
                        self.moveset.append(Move(move))

            if "ability" in mod:
                self.ability = Ability(mod["ability"])

            if "item" in mod:
                self.item = Item(mod["item"])

            if "status_main" in mod:
                self.status["main"] = mod["status_main"]

            if "status_sec" in mod:
                self.status["sec"] = mod["status_sec"]

            if "shiny" in mod:
                self.shiny = mod["shiny"][0]

            if "hp" in mod:
                self.hp = mod["hp"]

            if "max_hp" in mod:
                self.max_hp = mod["max_hp"]

    def init_moveset(self):
        moveset = []
        for move in self.movepool:
            if move["klass"] == "LevelLearnableMove":
                if move["level"] <= self.level:
                    if len(moveset) >= 4:
                        moveset.remove(random.choice(moveset))
                    moveset.append(Move(move["move"]))
        return moveset

    def init_stats(self, stat):
        if stat == "hp":
            return math.floor(((self.ivs[stat] + 2 * self.base_stats[stat] + math.floor(self.evs[stat] / 4)) *
                               self.level / 100) + self.level + 10)
        return math.floor((((self.ivs[stat] + 2 * self.base_stats[stat] + math.floor(self.evs[stat] / 4)) *
                            self.level / 100) + 5) * self.nature[stat])

    def update_hp(self):
        if self.damages_received:
            self.damages_received -= 1
            self.hp -= 1
            self.check_hp()

    def check_hp(self):
        if self.hp <= 0:
            self.hp = 0
            self.ko = True
            self.comments.append(str(self.name + " is ko !"))

    def exp_to_nxt_lvl(self):
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

    def calcul_damages(self, move, target):
        if move.power:
            # power
            hh = 1
            if self.status["sec"] == "helping hand":
                hh = 1.5
            it = 1
            if self.item:
                if self.item.name in DATA.plates:
                    if DATA.plates[self.item.name] == move.type.name:
                        it = 1.2
                elif self.item.name in DATA.type_enhancing_item:
                    if DATA.type_enhancing_item[self.item.name] == move.type.name:
                        it = 1.2
                elif self.item.name in DATA.type_enhancing_incences:
                    if DATA.type_enhancing_incences[self.item.name] == move.type.name:
                        it = 1.2
                elif self.item.name in DATA.gems:
                    if DATA.gems[self.item.name] == move.type.name:
                        it = 1.2
                elif self.item.name == "wise_glasses":
                    if move.category == "special":
                        it = 1.1
                elif self.item.name == "muscle_band":
                    if move.category == "physical":
                        it = 1.1
                elif self.item.name == "adamant_orb":
                    if self.name == "dialga":
                        if move.type.name == "steel" or move.type.name == "dragon":
                            it = 1.2
                elif self.item.name == "lustrous_orb":
                    if self.name == "palkia":
                        if move.type.name == "water" or move.type.name == "dragon":
                            it = 1.2
            chg = 1
            if self.charge and move.type.name == "electric":
                chg = 2
            ms = 1
            if self.mud_sport:
                ms = 0.5
            ws = 1
            if self.water_sport:
                ws = 0.5
            ua = 1
            if self.ability.name == "rivalry" and self.gender is not None and target.gender is not None:
                if target.gender is self.gender:
                    ua = 1.25
                if target.gender is not self.gender:
                    ua = 0.75
            elif self.ability.name == "blaze" and move.type.name == "fire" and self.hp <= self.max_hp / 3:
                ua = 1.5
            elif self.ability.name == "torrent" and move.type == "water" and self.hp <= self.max_hp / 3:
                ua = 1.5
            elif self.ability.name == "overgrow" and move.type == "grass" and self.hp <= self.max_hp / 3:
                ua = 1.5
            elif self.ability.name == "swarm" and move.type == "bug" and self.hp <= self.max_hp / 3:
                ua = 1.5
            if self.ability.name == "technician" and move.power <= 60:
                ua = 1.5
            if self.ability.name == "iron_fist":
                if move.feature["punch"]:
                    ua = 1.2
            if self.ability.name == "reckless":
                if move.battle_engine_method == "s_recoil":
                    ua = 1.2
            fa = 1
            if target.ability.name == "thick_fat":
                if move.type.name == "fire" or move.type.name == "ice":
                    fa = 0.5
            elif target.ability.name == "heatproof" and move.type == "fire":
                fa = 0.5
            elif target.ability.name == "dry_skin" and move.type.name == "fire":
                fa = 1.25
            power = hh * move.power * it * chg * ms * ws * ua * fa
            # atk
            move_category = self.ig_atk
            if move.category == "special":
                move_category = self.ig_aspe
            am = 1
            if move.category == "physical":
                if self.ability.name == "pure_power" or self.ability.name == "huge_power":
                    am = 2
                if self.ability.name == "guts":
                    if self.status["main"] == "paralysis" or self.status["main"] == "poisoning" or \
                            self.status["main"] == "burn" or self.status["main"] == "sleep":
                        am = 1.5
                elif self.ability.name == "hustle":
                    am = 1.5
            elif move.category == "special":
                pass
            im = 1
            if self.item:
                if move.category == "physical":
                    if self.item.name == "choice_band":
                        im = 1.5
                    if self.item.name == "light_ball" and self.name == "Pikachu":
                        im = 2
                    if self.item.name == "thick_club":
                        if self.name == "Cubone" or self.name == "Marowak":
                            im = 2
                elif move.category == "special":
                    if self.item.name == "choice_specs":
                        im = 1.5
                    if self.item.name == "light_ball" and self.name == "pikachu":
                        im = 2
                    if self.item.name == "soul_dew":
                        if self.name == "latios" or self.name == "latias":
                            im = 1.5
                    if self.item.name == "deep_sea_tooth" and self.name == "clamperl":
                        im = 2
            atk = move_category * am * im
            # deff
            target_deff = target.deff
            if move.category == "special":
                target_deff = target.dspe
            sx = 1
            if move.name == "explosion" or move.name == "self_destruct":
                sx = 0.5
            mod = 1
            if target.item:
                if move.category == "physical":
                    if target.item.name == "marvel_scale":
                        if target.status["main"] == "poisoning" or target.status["main"] == "sleep" or \
                                target.status["main"] == "paralysis" or target.status["main"] == "freeze" or \
                                target.status["main"] == "burn":
                            mod = 1.5
                elif move.category == "special":
                    if target.item.name == "soul_dew":
                        if target.name == "latios" or target.name == "latias":
                            mod = 1.5
                    elif target.item.name == "deep_sea_scale" and target.name == "clamperl":
                        mod = 2
            deff = target_deff * sx * mod
            # mod 1
            brn = 1
            if self.status["main"] == "burn":
                if move.category == "physical" and self.ability.name != "guts":
                    brn = 0.5
            rl = 1
            if target.reflect and move.category == "physical":
                rl = 0.5
            if target.light_screen and move.category == "special":
                rl = 0.5
            tvt = 1  # 2v2
            sr = 1
            if self.weather == "sun" and move.type.name == "fire":
                sr = 1.5
            if self.weather == "rain" and move.type.name == "fire":
                sr = 0.5
            if self.weather == "sun" and move.type.name == "water":
                sr = 0.5
            if self.weather == "rain" and move.type.name == "water":
                sr = 1.5
            ff = 1
            pass
            mod1 = brn * rl * tvt * sr * ff
            # mod 2
            mod2 = 1
            pass
            # critical hit
            crit = 1
            if random.uniform(0, 100) <= 6.25 * move.critical_rate:
                crit = 2
                self.comments.append("A critical hit !")
            # random
            r = (random.randint(217, 255) * 100) / 255
            if move.name == "spit_up":
                r = 100
            # stab
            stab = 1
            for t in self.type:
                if move.type.name == t.name:
                    stab = 2 if self.ability.name == "adaptability" else 1.5
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
            if target.ability.name == "solid_rock" or target.ability.name == "filter":
                if typeA + typeB > 2.5:
                    srf = 0.75
            eb = 1
            if self.item and self.item.name == "expert_belt" and typeA + typeB > 2.5:
                eb = 1.2
            tl = 1
            if self.ability.name == "tinted_lens" and typeA + typeB < 2:
                tl = 2
            trb = 1
            if target.item and target.item.name in DATA.rbset:
                if DATA.rbset[target.item.name] == move.type.name:
                    if typeA + typeB > 2.5:
                        trb = 0.5
            if target.item and target.item.name == "chilan_berry" and move.type.name == "normal":
                trb = 0.5
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

    def additional_effects(self, move, target):
        if move.boosts:
            pkmn = self
            for stat in self.boosts:
                if move.target == "user":
                    self.boosts[stat] += move.boosts[stat]
                elif move.target == "adjacent_pokemon":
                    pkmn = target
                    target.boosts[stat] += move.boosts[stat]

                if -6 <= self.boosts[stat] <= 6:
                    if move.boosts[stat] == 1:
                        self.comments.append((pkmn.name + "'s " + stat + " rose !"))
                    if move.boosts[stat] == 2:
                        self.comments.append((pkmn.name + "'s " + stat + " rose sharply !"))
                    if move.boosts[stat] >= 3:
                        self.comments.append((pkmn.name + "'s " + stat + " rose drastically !"))
                    if move.boosts[stat] == -1:
                        self.comments.append((pkmn.name + "'s " + stat + " fell !"))
                    if move.boosts[stat] == -2:
                        self.comments.append((pkmn.name + "'s " + stat + " harshly fell !"))
                    if move.boosts[stat] <= -3:
                        self.comments.append((pkmn.name + "'s " + stat + " severely fell !"))
                elif pkmn.boosts[stat] >= 6:
                    pkmn.boosts[stat] = 6
                    self.comments.append((pkmn.name + "'s " + stat + " won't go any higher !"))
                elif pkmn.boosts[stat] <= -6:
                    pkmn.boosts[stat] = -6
                    self.comments.append((pkmn.name + "'s " + stat + " won't go any lower! !"))

            pkmn.ig_atk = int(pkmn.atk * DATA.F_BOOSTS[pkmn.boosts["atk"] + 6])
            pkmn.ig_deff = int(pkmn.deff * DATA.F_BOOSTS[pkmn.boosts["deff"] + 6])
            pkmn.ig_aspe = int(pkmn.aspe * DATA.F_BOOSTS[pkmn.boosts["aspe"] + 6])
            pkmn.ig_dspe = int(pkmn.dspe * DATA.F_BOOSTS[pkmn.boosts["dspe"] + 6])
            pkmn.ig_spd = int(pkmn.spd * DATA.F_BOOSTS[pkmn.boosts["spd"] + 6])

    def attack(self, move, target):
        self.comments.clear()
        if self.can_attack(move, target):
            self.comments.append(str(self.name + " use " + move.name))
            move.pp -= 1
            if not move.accuracy or random.randint(0, 100) <= move.accuracy:
                dmgs = self.calcul_damages(move, target)
                target.damages_received = dmgs
                target.check_hp()
                self.additional_effects(move, target)
            else:
                self.comments.append("But it failed !")
