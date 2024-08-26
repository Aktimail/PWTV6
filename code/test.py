import random

from move import *


class Pokemon:
    def __init__(self, no, name, types, gender, ability, lvl, base_stats, evs, ivs, nature, moveset, item, tier):
        self.no = no
        self.name = name
        self.types = types
        self.gender = gender
        self.ability = ability

        self.lvl = lvl
        self.base_stats = base_stats
        self.evs = evs
        self.ivs = ivs
        self.nature = nature

        self.moveset = moveset
        self.ig_pps = {}
        for move in self.moveset:
            self.ig_pps[move] = move.pp

        self.item = item
        self.tier = tier

        self.hp = int(
            ((self.ivs["hp"] + 2 * self.base_stats["hp"] + (self.evs["hp"] // 4)) * self.lvl // 100) + self.lvl + 10)
        self.ig_hp = self.hp
        self.atk = int(
            (((self.ivs["atk"] + 2 * self.base_stats["atk"] + (self.evs["atk"] // 4)) * self.lvl // 100) + 5) *
            self.nature[1])
        self.ig_atk = self.atk
        self.deff = int(
            (((self.ivs["deff"] + 2 * self.base_stats["deff"] + (self.evs["deff"] // 4)) * self.lvl // 100) + 5) *
            self.nature[2])
        self.ig_deff = self.deff
        self.aspe = int(
            (((self.ivs["aspe"] + 2 * self.base_stats["aspe"] + (self.evs["aspe"] // 4)) * self.lvl // 100) + 5) *
            self.nature[3])
        self.ig_aspe = self.aspe
        self.dspe = int(
            (((self.ivs["dspe"] + 2 * self.base_stats["dspe"] + (self.evs["dspe"] // 4)) * self.lvl // 100) + 5) *
            self.nature[4])
        self.ig_dspe = self.dspe
        self.spd = int(
            (((self.ivs["spd"] + 2 * self.base_stats["spd"] + (self.evs["spd"] // 4)) * self.lvl // 100) + 5) *
            self.nature[5])
        self.ig_spd = self.spd

        self.boosts = {"atk": 0, "deff": 0, "aspe": 0, "dspe": 0, "spd": 0}
        self.status = {"main": None, "sec": None}
        self.ko = False

        self.charge = False
        self.mud_sport = False
        self.water_sport = False
        self.reflect = False
        self.light_screen = False

        self.weather = None

        self.ability_on = False
        self.item_on = False

    def show_info(self):
        print("N°" + str(self.no), self.name, end=""), print(
            " | " + str(self.status["main"]) if not self.status["main"] is None else "")
        print(str(self.ig_hp) + "/" + str(self.hp) + " hp")
        print("===============")
        print("Type(s) : ", end="")
        for t in self.types:
            print(t.name, "", end="")
        print()
        print("Gender :", self.gender, "| Lvl", self.lvl)
        print("Ability :", self.ability, "| Item :", self.item)
        print("===============")
        print("Stats :")
        stats_name = ["atk", "deff", "aspe", "dspe", "spd"]
        stats = [self.atk, self.deff, self.aspe, self.dspe, self.spd]
        for sn, s in zip(stats_name, stats):
            print(sn, ":", s, "", end="")
            for i in range(abs(self.boosts[sn])):
                if self.boosts[sn] > 0:
                    print("▲", end="")
                if self.boosts[sn] < 0:
                    print("▼", end="")
            for i in range(6 - abs(self.boosts[sn])):
                print("•", end="")
            print(end="\n")
        print("===============")
        print("Moves :")
        for m in self.moveset:
            print(m.name, str(self.ig_pps[m]) + "/" + str(m.pp))

    def valid(self):
        if 1 > self.lvl > 100:
            print(self.name, "ERROR\n Lvl must be less than 100.")
            input()
            return False
        for val in self.evs.values():
            if val > 252 or val < 0:
                print(self.name, "ERROR\n Evs must be less than 252 per stat.")
                input()
                return False
        if sum(self.evs.values()) > 510:
            print(self.name, "ERROR\n The sum of the evs must be less than 510.")
            input()
            return False
        for val in self.ivs.values():
            if val > 31 or val < 0:
                print(self.name, "ERROR\n Ivs must be less than 31 per stat.")
                input()
                return False
        if len(self.moveset) > 4:
            print(self.name, "ERROR\n Pokemon cannot have more than 4 moves.")
            input()
            return False
        return True

    def update_hp(self):
        if self.ig_hp <= 0:
            self.ig_hp, self.ko = 0, True
            delay_print((self.name + " is ko !"))
        else:
            delay_print((self.name + " is " + str(self.ig_hp) + "/" + str(self.hp) + " hp"))
            time.sleep(st)

    def can_attack(self, move: Move, target):
        if self.ko or move.pp <= 0:
            return False
        if self.status["main"] == sleep and move.name != "Sleep Talk":
            delay_print((self.name + " is fast asleep !")), time.sleep(st)
            return False
        if self.status["main"] == freeze:
            delay_print((self.name + " is frozen solid !")), time.sleep(st)
            return False
        if self.status["sec"] == flinch:
            delay_print((self.name + " flinched and couldn't move !")), time.sleep(st)
            return False
        if self.status["main"] == paralysis:
            delay_print((self.name + " is paralyzed !")), time.sleep(st)
            if random.randint(0, 100) <= 25:
                delay_print("It can't move !"), time.sleep(st)
                return False
        if self.status["sec"] == confusion:
            delay_print((self.name + " is confused !")), time.sleep(st)
            if random.randint(0, 100) <= 33:
                delay_print("It hurt itself in its confusion !"), time.sleep(st)
                self.ig_hp = int(self.ig_hp - (((((self.lvl * 2 / 5) + 2) * 40 * self.atk / 50) / self.deff) + 2) *
                                 ((random.randint(217, 255) * 100) / 255) / 100)
                self.update_hp()
                return False
        if self.status["sec"] == attract:
            delay_print((self.name + " is in love with " + target.name + " !")), time.sleep(st)
            if random.randint(0, 100) <= 50:
                delay_print(self.name + " is immobilized by love !"), time.sleep(st)
                return False
        return True

    def calcul_damages(self, move: Move, target):
        if move.base_power:
            # power
            hh = 1
            if "helping hand" in self.status:
                hh = 1.5
            it = 1
            if self.item in plates:
                if plates[self.item] == move.m_type:
                    it = 1.2
            elif self.item in type_enhancing_item:
                if type_enhancing_item[self.item] == move.m_type:
                    it = 1.2
            elif self.item in type_enhancing_incences:
                if type_enhancing_incences[self.item] == move.m_type:
                    it = 1.2
            elif self.item in gems:
                if gems[self.item] == move.m_type:
                    it = 1.2
            elif self.item == wise_glasses:
                if move.category == special:
                    it = 1.1
            elif self.item == muscle_band:
                if move.category == physical:
                    it = 1.1
            elif self.item == adamant_orb:
                if self.name == "Dialga":
                    if move.m_type == Steel_type or move.m_type == Dragon_type:
                        it = 1.2
            elif self.item == lustrous_orb:
                if self.name == "Palkia":
                    if move.m_type == Water_type or move.m_type == Dragon_type:
                        it = 1.2
            chg = 1
            if self.charge and move.m_type == Electric_type:
                chg = 2
            ms = 1
            if self.mud_sport:
                ms = 0.5
            ws = 1
            if self.water_sport:
                ws = 0.5
            ua = 1
            if self.ability == rivalry and self.gender is not None and target.gender is not None:
                if target.gender is self.gender:
                    ua = 1.25
                if target.gender is not self.gender:
                    ua = 0.75
            elif self.ability == blaze and move.m_type == Fire_type and self.ig_hp <= self.hp / 3:
                ua = 1.5
            elif self.ability == torrent and move.m_type == Water_type and self.ig_hp <= self.hp / 3:
                ua = 1.5
            elif self.ability == overgrow and move.m_type == Grass_type and self.ig_hp <= self.hp / 3:
                ua = 1.5
            elif self.ability == swarm and move.m_type == Bug_type and self.ig_hp <= self.hp / 3:
                ua = 1.5
            if self.ability == technician and move.base_power <= 60:
                ua = 1.5
            if self.ability == iron_fist:
                if move.name in punch_moves:
                    ua = 1.2
            if self.ability == reckless:
                if "recoil" in move.effect:
                    ua = 1.2
            fa = 1
            if target.ability == thick_fat:
                if move.m_type is Fire_type or move.m_type is Ice_type:
                    fa = 0.5
            elif target.ability == heatproof and move.m_type is Fire_type:
                fa = 0.5
            elif target.ability == dry_skin and move.m_type is Fire_type:
                fa = 1.25
            power = hh * move.base_power * it * chg * ms * ws * ua * fa
            # atk
            move_atk = self.ig_atk
            if move.category == special:
                move_atk = self.ig_aspe
            am = 1
            if move.category == physical:
                if self.ability == pure_power or self.ability == huge_power:
                    am = 2
                if self.ability == guts:
                    if self.status["main"] == paralysis or self.status["main"] == poisoning or \
                            self.status["main"] == burn or self.status["main"] == sleep:
                        am = 1.5
                elif self.ability == hustle:
                    am = 1.5
            elif move.category == special:
                pass
            im = 1
            if move.category == physical:
                if self.item == choice_band:
                    im = 1.5
                if self.item == light_ball and self.name == "Pikachu":
                    im = 2
                if self.item == thick_club:
                    if self.name == "Cubone" or self.name == "Marowak":
                        im = 2
            elif move.category == special:
                if self.item == choice_specs:
                    im = 1.5
                if self.item == light_ball and self.name == "Pikachu":
                    im = 2
                if self.item == soul_dew:
                    if self.name == "Latios" or self.name == "Latias":
                        im = 1.5
                if self.item == deep_sea_tooth and self.name == "Clamperl":
                    im = 2
            atk = move_atk * am * im
            # deff
            target_deff = target.ig_deff
            if move.category == special:
                target_deff = target.ig_dspe
            sx = 1
            if move.name == "Explosion" or move.name == "Self-Destruct":
                sx = 0.5
            mod = 1
            if move.category == physical:
                if target.item == marvel_scale:
                    if target.status["main"] == poisoning or target.status["main"] == sleep or \
                            target.status["main"] == paralysis or target.status["main"] == freeze or \
                            target.status["main"] == burn:
                        mod = 1.5
            elif move.category == special:
                if target.item == soul_dew:
                    if target.name == "latios" or target.name == "Latias":
                        mod = 1.5
                elif target.item == deep_sea_scale:
                    if target.name == "Clamperl":
                        mod = 2
            deff = target_deff * sx * mod
            # mod 1
            brn = 1
            if burn in self.status:
                if move.category == physical and self.ability != guts:
                    brn = 0.5
            rl = 1
            if target.reflect and move.category == physical:
                rl = 0.5
            if target.light_screen and move.category == special:
                rl = 0.5
            tvt = 1  # 2v2
            sr = 1
            if self.weather == sun and move.m_type == Fire_type:
                sr = 1.5
            if self.weather == rain and move.m_type == Fire_type:
                sr = 0.5
            if self.weather == sun and move.m_type == Water_type:
                sr = 0.5
            if self.weather == rain and move.m_type == Water_type:
                sr = 1.5
            ff = 1
            if self.ability == flash_fire:
                if self.ability_on and move.m_type == Fire_type:
                    ff = 1.5
            mod1 = brn * rl * tvt * sr * ff
            # mod 2
            mod2 = 1
            if self.item == life_orb:
                mod2 = 1.3
            if self.item == metronome and self.item_on:
                mod2 = self.item_on / 10 + 1
            if move.name == "Me First":
                mod2 = 1.5
            # critical hit
            crit = 1
            if random.uniform(0, 100) <= 6.25:
                crit = 3 if self.ability == sniper else 2
                delay_print("A critical hit !"), time.sleep(st)
            # random
            r = (random.randint(217, 255) * 100) / 255
            if move.name == "Spit Up":
                r = 100
            # stab
            stab = 1
            for t in self.types:
                if move.m_type == t:
                    stab = 1.5
                if self.ability is adaptability:
                    stab = 2
            # types
            typeA, typeB = 1, 1
            if move.m_type in target.types[0].immunities:
                typeA = 0
            elif move.m_type in target.types[0].resistances:
                typeA = 0.5
            elif move.m_type in target.types[0].weakness:
                typeA = 2
            if len(target.types) == 2:
                if move.m_type in target.types[1].immunities:
                    typeB = 0
                elif move.m_type in target.types[1].resistances:
                    typeB = 0.5
                elif move.m_type in target.types[1].weakness:
                    typeB = 2
            if typeA == 0 or typeB == 0:
                delay_print(("It doesn't affect " + target.name)), time.sleep(st)
            elif typeA + typeB < 2:
                delay_print("It's not very effective..."), time.sleep(st)
            elif typeA + typeB > 2.5:
                delay_print("It's super effective !"), time.sleep(st)
            # mod 3
            srf = 1
            if target.ability == solid_rock or target.ability == filter:
                if typeA + typeB > 2.5:
                    srf = 0.75
            eb = 1
            if self.item == expert_belt and typeA + typeB > 2.5:
                eb = 1.2
            tl = 1
            if self.ability == tinted_lens and typeA + typeB < 2:
                tl = 2
            trb = 1
            if target.item in rbset:
                if rbset[target.item] == move.m_type:
                    if typeA + typeB > 2.5:
                        trb = 0.5
            if target.item == chilan_berry and move.m_type == Normal_type:
                trb = 0.5
            mod3 = srf * eb * tl * trb
            # calcul
            dmgs = int(self.lvl * 2 / 5)
            dmgs = int(dmgs) + 2
            dmgs = int(dmgs) * power * atk / 50
            dmgs = int(dmgs) / deff
            dmgs = int(dmgs) * mod1
            dmgs = int(dmgs) + 2
            dmgs = int(dmgs) * crit * mod2 * r / 100
            dmgs = int(int(dmgs) * stab * typeA * typeB * mod3)
            return dmgs
        return 0

    def additional_effect(self, move: Move, target, dmgs):
        if move.effect:
            if self_boost in move.effect and move.effect[self_boost][1] >= random.randint(0, 100):
                for s in move.effect[self_boost][0].keys():
                    self.boosts[s] += move.effect[self_boost][0][s]
                    if -6 <= self.boosts[s] <= 6:
                        if move.effect[self_boost][0][s] == 1:
                            delay_print((self.name + "'s " + s + " rose !")), time.sleep(st)
                        if move.effect[self_boost][0][s] == 2:
                            delay_print((self.name + "'s " + s + " rose sharply !")), time.sleep(st)
                        if move.effect[self_boost][0][s] >= 3:
                            delay_print((self.name + "'s " + s + " rose drastically !")), time.sleep(st)
                        if move.effect[self_boost][0][s] == -1:
                            delay_print((self.name + "'s " + s + " fell !")), time.sleep(st)
                        if move.effect[self_boost][0][s] == -2:
                            delay_print((self.name + "'s " + s + " harshly fell !")), time.sleep(st)
                        if move.effect[self_boost][0][s] <= -3:
                            delay_print((self.name + "'s " + s + " severely fell !")), time.sleep(st)
                    elif self.boosts[s] >= 6:
                        self.boosts[s] = 6
                        delay_print((self.name + "'s " + s + " won't go any higher !")), time.sleep(st)
                    elif self.boosts[s] <= -6:
                        self.boosts[s] = -6
                        delay_print((self.name + "'s " + s + " won't go any lower! !")), time.sleep(st)
                self.ig_atk = int(self.atk * f_boost[self.boosts["atk"] + 6])
                self.ig_deff = int(self.deff * f_boost[self.boosts["deff"] + 6])
                self.ig_aspe = int(self.aspe * f_boost[self.boosts["aspe"] + 6])
                self.ig_dspe = int(self.dspe * f_boost[self.boosts["dspe"] + 6])
                self.ig_spd = int(self.spd * f_boost[self.boosts["spd"] + 6])
            if target_boost in move.effect and move.effect[target_boost][1] >= random.randint(0, 100):
                for s in move.effect[target_boost][0].keys():
                    self.boosts[s] += move.effect[target_boost][0][s]
                    if -6 <= target.boosts[s] <= 6:
                        if move.effect[target_boost][0][s] == 1:
                            delay_print((target.name + "'s " + s + " rose !")), time.sleep(st)
                        if move.effect[target_boost][0][s] == 2:
                            delay_print((target.name + "'s " + s + " rose sharply !")), time.sleep(st)
                        if move.effect[target_boost][0][s] >= 3:
                            delay_print((target.name + "'s " + s + " rose drastically !")), time.sleep(st)
                        if move.effect[target_boost][0][s] == -1:
                            delay_print((target.name + "'s " + s + " fell !")), time.sleep(st)
                        if move.effect[target_boost][0][s] == -2:
                            delay_print((target.name + "'s " + s + " harshly fell !")), time.sleep(st)
                        if move.effect[target_boost][0][s] <= -3:
                            delay_print((target.name + "'s " + s + " severely fell !")), time.sleep(st)
                    elif target.boosts[s] >= 6:
                        target.boosts[s] = 6
                        delay_print((target.name + "'s " + s + " won't go any higher !")), time.sleep(st)
                    elif target.boosts[s] <= -6:
                        target.boosts[s] = -6
                        delay_print((target.name + "'s " + s + " won't go any lower! !")), time.sleep(st)
                target.ig_atk = int(target.atk * f_boost[target.boosts["atk"] + 6])
                target.ig_deff = int(target.deff * f_boost[target.boosts["deff"] + 6])
                target.ig_aspe = int(target.aspe * f_boost[target.boosts["aspe"] + 6])
                target.ig_dspe = int(target.dspe * f_boost[target.boosts["dspe"] + 6])
                target.ig_spd = int(target.spd * f_boost[target.boosts["spd"] + 6])

            if recoil in move.effect:
                delay_print((self.name + " is damaged by recoil !")), time.sleep(st)
                self.ig_hp = int(self.ig_hp - dmgs * move.effect[recoil])
                self.update_hp()

            if self_status in move.effect:
                if random.randint(0, 100) <= move.effect[self_status][1]:
                    self.status["main"] = move.effect[self_status][0]
                    delay_print((self.name + " is " + move.effect[self_status][0]))

            if target_status in move.effect:
                if random.randint(0, 100) <= move.effect[target_status][1]:
                    target.status["main"] = move.effect[target_status][0]
                    delay_print((target.name + " is " + move.effect[target_status][0]))

    def attack(self, move: Move, target):
        if self.can_attack(move, target):
            delay_print((self.name + " use " + move.name)), time.sleep(st)
            self.ig_pps[move] -= 1
            if move.m_accuracy is None or random.randint(0, 100) <= move.m_accuracy:
                if move.m_type == status:
                    pass
                else:
                    dmgs = self.calcul_damages(move, target)
                    target.ig_hp -= dmgs
                    target.update_hp()
                    self.additional_effect(move, target, dmgs)
            else:
                delay_print("But it failed !")
        return self.name, move.name, target.name


# pokemons
"""Chandelure = Pokemon(609, "Chandelure", (Fire_type, Ghost_type), male, flash_fire, 100,
                     {"hp": 60, "atk": 55, "deff": 90, "aspe": 145, "dspe": 90, "spd": 80},  # stats
                     {"hp": 0, "atk": 0, "deff": 252, "aspe": 252, "dspe": 0, "spd": 6},  # evs
                     {"hp": 31, "atk": 31, "deff": 31, "aspe": 31, "dspe": 31, "spd": 31},  # ivs
                     modest, [Ancient_Power, Hyper_Beam, Fire_Blast], None, None)
Garchomp = Pokemon(445, "Garchomp", (Dragon_type, Ground_type), male, sand_veil, 100,
                   {"hp": 108, "atk": 130, "deff": 95, "aspe": 80, "dspe": 85, "spd": 102},
                   {"hp": 0, "atk": 252, "deff": 6, "aspe": 0, "dspe": 0, "spd": 252},
                   {"hp": 31, "atk": 31, "deff": 31, "aspe": 31, "dspe": 31, "spd": 31},
                   modest, [Pound], None, over_used)
"""