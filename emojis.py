heroes_emojis = {
    "Alvanor": "hero_alvanor",
    "Amira": "hero_amira",
    "Andvari": "hero_andi",
    "Arachne": "hero_arachne",
    "Artemis": "hero_artemis",
    "Astaroth": "hero_asta",
    "Aurora": "hero_aurora",
    "Celeste": "hero_celeste",
    "Cleaver": "hero_cleaver",
    "Cornelius": "hero_cornelius",
    "Corvus": "hero_corvus",
    "Dante": "hero_dante",
    "Daredevil": "hero_daredevil",
    "Dark": "hero_darkstar",
    "Dorian": "hero_dorian",
    "Elmir": "hero_elmir",
    "Faceless": "hero_faceless",
    "Fafnir": "hero_fafnir",
    "Fox": "hero_fox",
    "Galahad": "hero_galahad",
    "Ginger": "hero_ginger",
    "Helios": "hero_helios",
    "Isaac": "hero_Isaac",
    "Ishmael": "hero_ishmael",
    "Jet": "hero_jet",
    "Jhu": "hero_jhu",
    "Jorgen": "hero_jorgen",
    "Judge": "hero_judge",
    "Kai": "hero_kai",
    "K'arkh": "hero_karkh",
    "Keira": "hero_keira",
    "Krista": "hero_krista",
    "Lars": "hero_lars",
    "Lian": "hero_lian",
    "Lilith": "hero_lilith",
    "Luther": "hero_lilith",
    "Markus": "hero_markus",
    "Martha": "hero_martha",
    "Morrigan": "hero_morrigan",
    "Nebula": "hero_nebula",
    "Orion": "hero_orion",
    "Peppy": "hero_peppy",
    "Phobos": "hero_phobos",
    "Qing": "hero_qingmao",
    "Rufus": "hero_rufus",
    "Satori": "hero_satori",
    "Sebastian": "hero_sebastian",
    "Tristan": "hero_tristan",
    "Xe'Sha": "hero_xesha",
    "Yasmine": "hero_yasmine",
    "Ziri": "hero_ziri",
}

server_emojis = {
    "hero_alvanor": "<:hero_alvanor:990179342946545734>",
    "hero_amira": "<:hero_amira:990179344309710888>",
    "hero_andi": "<:hero_andi:989226933042704414>",
    "hero_arachne": "<:hero_arachne:989226934540054598>",
    "hero_artemis": "<:hero_artemis:989226935982903327>",
    "hero_asta": "<:hero_asta:989226937153110068>",
    "hero_aurora": "<:hero_aurora:989226939644518430>",
    "hero_celeste": "<:hero_celeste:989226941171245107>",
    "hero_cleaver": "<:hero_cleaver:989226943465545728>",
    "hero_cornelius": "<:hero_cornelius:989226944551870494>",
    "hero_corvus": "<:hero_corvus:989226945562693672>",
    "hero_dante": "<:hero_dante:989226946518978560>",
    "hero_daredevil": "<:hero_daredevil:989226948024737823>",
    "hero_darkstar": "<:hero_darkstar:989226949505318972>",
    "hero_dorian": "<:hero_dorian:989226951522811914>",
    "hero_elmir": "<:hero_elmir:989226952382619699>",
    "hero_faceless": "<:hero_faceless:989226954014220398>",
    "hero_fafnir": "<:hero_fafnir:990179378535215164>",
    "hero_fox": "<:hero_fox:989226955062796318>",
    "hero_galahad": "<:hero_galahad:989226955641593890>",
    "hero_ginger": "<:hero_ginger:989226957201866822>",
    "hero_helios": "<:hero_helios:989226959395512321>",
    "hero_ishmael": "<:hero_ishmael:989226960855138314>",
    "hero_jet": "<:hero_jet:989226962197295164>",
    "hero_jhu": "<:hero_jhu:989226963422052352>",
    "hero_jorgen": "<:hero_jorgen:989226964537737266>",
    "hero_judge": "<:hero_judge:989226966047658034>",
    "hero_kai": "<:hero_kai:989226967322726521>",
    "hero_karkh": "<:hero_karkh:989226968337743883>",
    "hero_keira": "<:hero_keira:989226969629618176>",
    "hero_krista": "<:hero_krista:989226970925649990>",
    "hero_lars": "<:hero_lars:989226972070699048>",
    "hero_lian": "<:hero_lian:989226973324787722>",
    "hero_lilith": "<:hero_lilith:989226974574706729>",
    "hero_luther": "<:hero_luther:989226975925260308>",
    "hero_markus": "<:hero_markus:989226977019961434>",
    "hero_martha": "<:hero_martha:989226978076938260>",
    "hero_morrigan": "<:hero_morrigan:989226981746950205>",
    "hero_nebula": "<:hero_nebula:989226983152054292>",
    "hero_orion": "<:hero_orion:989226984414539866>",
    "hero_peppy": "<:hero_peppy:989226985861558292>",
    "hero_phobos": "<:hero_phobos:989226987002396692>",
    "hero_qingmao": "<:hero_qingmao:989226988277473310>",
    "hero_rufus": "<:hero_rufus:989226989758066768>",
    "hero_satori": "<:hero_satori:989226990819242075>",
    "hero_sebastian": "<:hero_sebastian:989226991934902343>",
    "hero_tristan": "<:hero_tristan:990184097982849024>",
    "hero_xesha": "<:hero_xesha:990184272059043890>",
    "hero_yasmine": "<:hero_yasmine:990184009030041671>",
    "hero_ziri": "<:hero_ziri:989226994975789057>"
}

def get_hero_emoji(hero_name):
    if hero_name in heroes_emojis.keys():
        emoji_name = heroes_emojis[hero_name]
        
        if emoji_name in server_emojis.keys():
            return server_emojis[emoji_name]

        return emoji_name.replace('hero_')
    return hero_name