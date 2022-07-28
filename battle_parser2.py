import datetime
import hashlib
import json
import logger
import os.path
import re 
import storage

heroes_position = ["Chabba","Aurora","Cleaver","Luther","Corvus","Ziri","Rufus","Astaroth","Galahad","Tristan","Ishmael","Karkh","K'arkh","Markus","Elmir","Lilith","Andvari","Yasmine","Qing","Qing Mao","Satori","Alvanor","Maya","Arachne","Dante","Krista","Keira","Judge","Morrigan","Celeste","Kai","Jhu","Sebastian","Nebula","Mojo","Heidi","Jorgen","XeSha","Xe'Sha","Amira","Isaac","Orion","Daredevil","Ginger","DarkStar","Dark Star","Lars","Astrid", "Astrid and Lucas","Cornelius","Faceless","Fox","Lian","Phobos","Artemis","Dorian","Peppy","Jet","Thea","Fafnir","Helios","Martha"]
heroes_simplified = {
    "Astrid and Lucas": "Astrid",
    "Qing Mao": "Qing",
    "K'arkh": "Karkh",
    "Xe'Sha": "XeSha",
    "Dark Star": "DarkStar"
}

# Members
#re_ud_members = ".*(bbbbb1991|Col3|Mami|totobreizh|Jay|Sabre|Shaman|Stan|iosing|Leonidas|LukeNico|Crazy|Arkantos|NESS|Gah|Momonga|Oskidoki|LGCACC|LIVER|spgs91|Slayer|Mirkwood|HiatusB|TheWolf|HiatusB|KaMaL|Thrux|nater|pspman99|Elf|Fury).*"

def parse_text(texts, image_url, poster):
    result = {
        'battle': {
            'offensive_team': {
                'heroes': []
            },
            "defensive_team": {
                'heroes': []
            },
            "poster": poster,
            "posted_at": datetime.datetime.now().strftime("%x"),
            "image_url": image_url
        },
        "index": {
            "record_id": "1"
        },
    }
    
    # Sha256 to test unik battle
    compute_unik(result, texts)

    # split the image in zones
    zones = compute_zones(result,texts)

    # get texts by zones
    top_left = filter_by_zone(texts, zones, 'top_left')
    top_right = filter_by_zone(texts, zones, 'top_right')
    offensive_team = split_by_columns(filter_by_zone(texts, zones, 'offensive_team'))
    defensive_team = split_by_columns(filter_by_zone(texts, zones, 'defensive_team'))

    # get infos from top zone
    top_zone(result, top_left, 'offensive_team')
    top_zone(result, top_right, 'defensive_team')

    # get teams, heroes and powers
    get_offensive_team(result, offensive_team, 'offensive_team')
    get_defensive_team(result, defensive_team, 'defensive_team')

    # Compute team power
    compute_team_power(result, 'offensive_team')
    compute_team_power(result, 'defensive_team')

    # Compute index
    compute_team_index(result, 'offensive_team')
    compute_team_index(result, 'defensive_team')

    storage.store_battle(result)

    return result


def compute_unik(result, texts):
    hash_object = hashlib.sha256(str(texts).encode('utf-8'))
    result['index']['unik'] = hash_object.hexdigest()


def get_offensive_team(result, offensive_team, team):
    for hero in offensive_team:
        result['battle'][team]['heroes'].append({
            'name': hero[0],
            'power': int(hero[1].replace('X','').replace(' ', ''))
        })

def get_defensive_team(result, defensive_team, team):
    for hero in defensive_team:
        result['battle'][team]['heroes'].append({
            'name': hero[1],
            'power': int(hero[0].replace('X','').replace(' ', ''))
        })

def top_zone(result, lines, team):
    
    # Training == no info
    if (len(lines) == 0):
        result['index']['type'] = 'training'
        return

    # If server is present => war
    for line in lines:
        for text in line:
            if 'Server' in text['text']:
                result['index']['type'] = 'war'
                break

    # Else Arena
    if 'type' not in result['index'].keys() or result['index']['type'] == 'arena':
        result['index']['type'] = 'arena'
        top_zone_arena(result, lines, team)
    elif result['index']['type'] == 'war':
        top_zone_war(result, lines, team)


def top_zone_arena(result, lines, team):
    result['battle'][team]['player'] = ' '.join([x['text'] for x in lines[0]])
    result['battle'][team]['guild'] = ' '.join([x['text'] for x in lines[1]])


def top_zone_war(result, lines, team):
    line_1 = lines[0]
    line_2 = lines[1]

    # Get server, player and guild
    if team == 'offensive_team':
        result['battle'][team]['server'] = line_1[2]['text']
        
        i=3
        player=[]
        while i < len(line_1)-1:
            player.append(line_1[i]['text'])
            i+=1
        result['battle'][team]['player'] = ' '.join([str(x) for x in player])

        i=0
        guild=[]
        while i < len(line_2[0]):
            guild.append(line_2[i]['text'])
            i+=1
        result['battle'][team]['guild'] = ' '.join([str(x) for x in guild])
    elif team == 'defensive_team':
        result['battle'][team]['server'] = line_1[-1]['text']

        i=0
        player=[]
        while i < len(line_1)-3:
            player.append(line_1[i]['text'])
            i+=1
        result['battle'][team]['player'] = ' '.join([str(x) for x in player])

        i=0
        guild=[]
        while i <= len(line_2[0]):
            guild.append(line_2[i]['text'])
            i+=1
        result['battle'][team]['guild'] = ' '.join([str(x) for x in guild])


def filter_by_zone(texts, zones, zone):
    z_filters = zones[zone]
    z_texts = []
    log_enabled = False
    for text in texts:
        if 'top' in z_filters and z_filters['top'] >= text['b0.y']:
            logger.log("\t out: "+text['text']+"z_filters['top']="+str(z_filters['top']) + " < text['b0.y']="+str(text['b0.y']), log_enabled)
            continue
        elif 'top' in z_filters:
            logger.log("\t in: "+text['text']+" z_filters['top']="+str(z_filters['top']) + " < text['b0.y']="+str(text['b0.y']), log_enabled)
        if 'left' in z_filters and z_filters['left'] >= text['b0.x']:
            logger.log("\t out: "+text['text']+"z_filters['left']="+str(z_filters['left']) + " < text['b0.x']="+str(text['b0.x']), log_enabled)
            continue
        elif 'left' in z_filters:
            logger.log("\t in: "+text['text']+" z_filters['left']="+str(z_filters['left']) + " < text['b0.x']="+str(text['b0.x']), log_enabled)
        if 'right' in z_filters and z_filters['right'] <= text['b1.x']:
            logger.log("\t out: "+text['text']+"z_filters['right']="+str(z_filters['right']) + " < text['b1.x']="+str(text['b1.x']), log_enabled)
            continue
        elif 'right' in z_filters:
            logger.log("\t in: "+text['text']+" z_filters['right']="+str(z_filters['right']) + " < text['b1.x']="+str(text['b1.x']), log_enabled)
        if 'bottom' in z_filters and z_filters['bottom'] <= text['b3.y']:
            logger.log("\t out: "+text['text']+"z_filters['bottom']="+str(z_filters['bottom']) + " < text['b3.y']="+str(text['b3.y']), log_enabled)
            continue
        elif 'bottom' in z_filters:
            logger.log("\t in: "+text['text']+" z_filters['bottom']="+str(z_filters['bottom']) + " < text['b3.y']="+str(text['b3.y']), log_enabled)
        
        z_texts.append(text)

    logger.log('### z_texts: '+zone, log_enabled)
    logger.log(z_texts, log_enabled)

    return merge_by_lines(z_texts, zone)

def merge_by_lines(z_texts, zone):
    m_texts = []
    previous_b2_y = 0
    i=0
    while i < len(z_texts):
        text = z_texts[i]
        current_b2_y = text['b2.y']
        if previous_b2_y == 0:
            m_texts.append([{
                'text': text['text'],
                'x': text['b3.x']
            }])
            previous_b2_y = current_b2_y
            i+=1
        elif previous_b2_y + 15 >= current_b2_y and previous_b2_y - 15 <= current_b2_y:
            m_texts[len(m_texts)-1].append({
                'text': text['text'],
                'x': text['b3.x']
            })
            i+=1
        else:
            previous_b2_y = 0

    return sort_lines(m_texts)


def sort_lines(m_texts):
    for line in m_texts:
        line.sort(key= lambda x: x.get('x'))
    return m_texts

def split_by_columns(s_texts):
    log_enabled = False
    # column bounds
    line = s_texts[0]
    
    min_x = line[0]['x'] + 25
    max_x = line[len(line)-1]['x'] - 25
    mid_x = int((max_x + min_x) / 2)

    c_texts = []
    i=0
    while i < len(s_texts):
        line = s_texts[i]

        logger.log('min_x: '+str(min_x)+' > '+str(line), log_enabled)
        # ignore damage line
        if min_x < line[0]['x']:
            i+=1
            continue

        # get first column
        y = 0
        col_1 = []
        col_2 = []
        while y < len(line):
            if line[y]['x'] > mid_x:
                break
            col_1.append(line[y]['text'])
            y+=1

        # get second column
        while y < len(line):
            col_2.append(line[y]['text'])
            y+=1

        c_texts.append([
            ' '.join([str(x) for x in col_1]), 
            ' '.join([str(x) for x in col_2])
        ])

        i+=1

    return c_texts


def compute_zones(result, texts):
    battle_res1_tab = search(texts, ['Victory', 'Defeat', 'Draw'])
    battle_res1 = battle_res1_tab[0]
    battle_res2 = search(texts, ['Victory', 'Defeat', 'Draw'], battle_res1_tab[1]+1)[0]

    result['battle']['offensive_team']['result'] = battle_res1['text']
    result['battle']['defensive_team']['result'] = battle_res2['text']

    mid_x = int((battle_res1['b0.x'] + battle_res2['b1.x'])/2)
    #print('mid_x:'+str(mid_x))

    return {
        'top_left': {
            'left': int(battle_res1['b0.x']/2),
            'right': mid_x,
            'bottom': 2 * battle_res1['b0.y'] - battle_res1['b3.y']
        },
        'top_right': {
            'right': 2 * battle_res2['b1.x'] - battle_res2['b0.x'],
            'left': mid_x,
            'bottom': 2 * battle_res1['b0.y'] - battle_res1['b3.y']
        },
        'offensive_team': {
            'top': battle_res1['b3.y'],
            'left': battle_res1['b1.x'],
            'right': mid_x
        },
        'defensive_team': {
            'top': battle_res2['b2.y'],
            'left': mid_x,
            'right': battle_res2['b0.x']
        }
    }


def compute_team_power(result, team):
    pwr = 0
    for hero in result['battle'][team]['heroes']:
        pwr = pwr + int(hero['power'])
    
    result['battle'][team]['power'] = int(pwr / 1000)

def compute_team_index(result, team):
    index = ""
    for hero_pos in heroes_position:
        for hero in result['battle'][team]['heroes']:
            if hero['name'] == hero_pos:
                hero_index = hero_pos
                if hero_pos in heroes_simplified.keys():
                    hero_index = heroes_simplified[hero_pos]
                index = index + ';' + hero_index + ';'
    result['index'][team] = index

def search(texts, search_tokens, i=0):
    text = None
    while i < len(texts):
        text = texts[i]
        
        found = False
        for token in search_tokens:
            if text['text'].startswith(token):
                found = True
                break
        if found:
            break

        i+=1
    return [text, i]