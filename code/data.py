class DATA:
    ENTITIES_DESTINATIONS = {}

    F_BOOSTS = [0.25, 0.29, 0.33, 0.4, 0.5, 0.66, 1, 1.5, 2, 2.5, 3, 3.5, 4]

    ALL_NATURES = {
        "hardy": {"atk": 1, "deff": 1, "aspe": 1, "dspe": 1, "spd": 1},
        "lonely": {"atk": 1.1, "deff": 0.9, "aspe": 1, "dspe": 1, "spd": 1},
        "brave": {"atk": 1.1, "deff": 1, "aspe": 1, "dspe": 1, "spd": 0.9},
        "adamant": {"atk": 1.1, "deff": 1, "aspe": 0.9, "dspe": 1, "spd": 1},
        "naughty": {"atk": 1.1, "deff": 1, "aspe": 1, "dspe": 0.9, "spd": 1},
        "bold": {"atk": 0.9, "deff": 1.1, "aspe": 1, "dspe": 1, "spd": 1},
        "docile": {"atk": 1, "deff": 1, "aspe": 1, "dspe": 1, "spd": 1},
        "relaxed": {"atk": 1, "deff": 1.1, "aspe": 1, "dspe": 1, "spd": 0.9},
        "impish": {"atk": 1, "deff": 1.1, "aspe": 0.9, "dspe": 1, "spd": 1},
        "lax": {"atk": 1, "deff": 1.1, "aspe": 0.9, "dspe": 1, "spd": 1},
        "timid": {"atk": 0.9, "deff": 1, "aspe": 1, "dspe": 1, "spd": 1.1},
        "hasty": {"atk": 1, "deff": 0.9, "aspe": 1, "dspe": 1, "spd": 1.1},
        "serious": {"atk": 1, "deff": 1, "aspe": 1, "dspe": 1, "spd": 1},
        "jolly": {"atk": 1, "deff": 1, "aspe": 0.9, "dspe": 1, "spd": 1.1},
        "naive": {"atk": 1, "deff": 1, "aspe": 1, "dspe": 0.9, "spd": 1.1},
        "modest": {"atk": 0.9, "deff": 1, "aspe": 1.1, "dspe": 1, "spd": 1},
        "mild": {"atk": 1, "deff": 0.9, "aspe": 1.1, "dspe": 1, "spd": 1},
        "quiet": {"atk": 1, "deff": 1, "aspe": 1.1, "dspe": 1, "spd": 0.9},
        "bashful": {"atk": 1, "deff": 1, "aspe": 1, "dspe": 1, "spd": 1},
        "rash": {"atk": 1, "deff": 1, "aspe": 1.1, "dspe": 0.9, "spd": 1},
        "calm": {"atk": 0.9, "deff": 1, "aspe": 1, "dspe": 1.1, "spd": 1},
        "gentle": {"atk": 1, "deff": 0.9, "aspe": 1, "dspe": 1.1, "spd": 1},
        "sassy": {"atk": 1, "deff": 1, "aspe": 1, "dspe": 1, "spd": 1},
        "careful": {"atk": 1, "deff": 1, "aspe": 1, "dspe": 1.1, "spd": 0.9},
        "quirky": {"atk": 1, "deff": 1, "aspe": 1, "dspe": 1, "spd": 1},
    }

    plates = {
        "fist_plate": "fighting",
        "dread_plate": "dark",
        "flame_plate": "fire",
        "draco_plate": "dragon",
        "stone_plate": "rock_type",
        "zap_plate": "electric",
        "iron_plate": "steel",
        "meadow_plate": "grass",
        "splash_plate": "water",
        "icicle_plate": "ice",
        "toxic_plate": "poison",
        "sky_plate": "flying",
        "blank_plate": "normal",
        "insect_plate": "bug",
        "earth_plate": "ground",
        "spooky_plate": "ghost",
        "mind_plate": "psychic"
    }

    type_enhancing_item = {
        "black_belt": "fighting",
        "black_glasses": "dark",
        "charcoal": "fire",
        "dragon_fang": "dragon",
        "hard_stone": "rock",
        "magnet": "electric",
        "metal_coat": "steel",
        "miracle_seed": "grass",
        "mystic_water": "water",
        "never_melt_ice": "ice",
        "poison_barb": "poison",
        "sharp_beak": "flying",
        "silk_scarf": "normal",
        "silver_powder": "bug",
        "soft_sand": "ground",
        "spell_tag": "ghost",
        "twisted_spoon": "psychic"
    }

    type_enhancing_incences = {
        "odd_incense": "psychic",
        "rock_incense": "rock",
        "rose_incense": "grass",
        "sea_incense": "water",
        "wave_incense": "water"
    }

    gems = {
        "bug_gem": "bug",
        "dark_gem": "dark",
        "dragon_gem": "dragon",
        "electric_gem": "electric",
        "fairy_gem": "fairy",
        "fighting_gem": "fighting",
        "fire_gem": "fire",
        "flying_gem": "flying",
        "ghost_gem": "ghost",
        "grass_gem": "grass",
        "ground_gem": "ground",
        "ice_gem": "ice",
        "normal_gem": "normal",
        "poison_gem": "poison",
        "psychic_gem": "psychic",
        "rock_gem": "rock",
        "steel_gem": "steel",
        "water_gem": "water"
    }

    rbset = {
        "occa_berry": "fire",
        "passho_berry": "water",
        "wacan_berry": "electric",
        "rindo_berry": "grass",
        "yache_berry": "ice",
        "chople_berry": "fighting",
        "kebia_berry": "poison",
        "shuca_berry": "ground",
        "coba_berry": "flying",
        "iapapa_berry": "psychic",
        "tanga_berry": "bug",
        "charti_berry": "rock",
        "kasib_berry": "ghost",
        "haban_berry": "dragon",
        "colbur_berry": "dark",
        "babiri_berry": "steel"
    }
