import hashlib
import json
import os.path
import re 

heroes_position = ["Chabba","Aurora","Cleaver","Luther","Corvus","Ziri","Rufus","Astaroth","Galahad","Tristan","Ishmael","K'arkh","Markus","Elmir","Lilith","Andvari","Yasmine","Qing Mao","Satori","Middle Line","Alvanor","Maya","Arachne","Dante","Krista","Keira","Judge","Morrigan","Celeste","Kai","Jhu","Sebastian","Nebula","Mojo","Heidi","Jorgen","Xe'Sha","Isaac","Orion","Daredevil","Ginger","Darkstar","Lars","Astrid & Lucas","Cornelius","Faceless","Fox","Lian","Phobos","Artemis","Dorian","Peppy","Jet","Thea","Helios","Martha"]
heroes_list_re = ".*(Aurora|Astaroth|Luther|Cleaver|Galahad|Andvari|Fafnir|Ziri|Rufus|Corvus|Chabba|Martha|Dorian|Markus|Thea|Celeste|Nebula|Jorgen|Faceless|Helios|Sebastian|Alvanor|Judge|Tristan|Morrigan|Isaac|Mojo|Lars|Krista|Satori|Lilith|Orion|Peppy|Arachne|Kai|K’arkh|Cornelius|Dark|Elmir|Daredevil|Ginger|Dante|Fox|Ishmael|Jhu|Artemis|Astrid|Keira|Yasmine|Qing|Maya|Lian|Phobos|Heidi).*"

def parse_text(texts, image_url):
    result = {
        "offensive_team": {
            'heroes': []
        },
        "deffensive_team": {
            'heroes': []
        },
        "_image_url": image_url
    }
    
    # Sha256 to test unik battle
    compute_unik(result, texts)

    # log the input
    if os.path.exists('logs/'+result['_unik']+'-input.txt'):
        return {'message': 'battle already processed'}

    f = open('logs/'+result['_unik']+'-input.txt', "a")
    for text in texts:
        f.write(text+'\n')
    f.close()

    # Parse teams
    get_team(result, texts, 'offensive_team')
    get_team(result, texts, 'deffensive_team')

    # Parse results
    get_result(result, texts, 'offensive_team')
    get_result(result, texts, 'deffensive_team')

    # compute the x middle of the screenshot
    x_mid = get_x_mid(result, texts)

    # Parse powers
    get_power(result, texts, 'offensive_team', x_mid)

    # Compute team power
    compute_team_power(result, 'offensive_team')
    compute_team_power(result, 'deffensive_team')

    # Compute index
    compute_team_index(result, 'offensive_team')
    compute_team_index(result, 'deffensive_team')
    
    # log the input
    f = open('logs/'+result['_unik']+"-output.txt", "a")
    f.write(json.dumps(result, indent=4, sort_keys=True))
    f.close()

    return result

def compute_unik(result, texts):
    hash_object = hashlib.sha256(str(texts).encode('utf-8'))
    result['_unik'] = hash_object.hexdigest()

def get_team(result, texts, team):
    i = team_jump(texts, team)

    while i < len(texts):
        block = readblock(texts[i], texts[i+1])

        if 'Damage' in block['text']:
            break

        hero = re.findall(heroes_list_re, block['text'])
        if 0 < len(hero):
            result[team]['heroes'].append({
                'name': hero[0]
            })
        
        i=i+2

def get_power(result, texts, team, x_mid):
    # 3rd Damage occurence
    i = jump(texts, ['Damage'], 0)
    i = jump(texts, ['Damage'], i)
    i = jump(texts, ['Damage'], i)

    previous_x_max = 0
    previous_pwr = ""
    count_offensive=0
    count_deffensive=0

    while i < len(texts):
        block = readblock(texts[i], texts[i+1])
        i=i+2

        #print('text:',block['text'], 'previous:',previous_pwr)

        pwrs = re.findall("\d+", block['text'])
        if 0 < len(pwrs):
            pwr = pwrs[0]

            x_min = int(block['bounds'][0])
            x_max = int(block['bounds'][2])

            if x_min - previous_x_max < 7 \
                and x_min - previous_x_max > -7 \
                and x_max <= x_mid:
                result['offensive_team']['heroes'][count_offensive]['power'] = previous_pwr+pwr
                count_offensive=count_offensive+1
                previous_x_max = 0
                previous_pwr = ""
            elif x_min - previous_x_max < 7 \
                and x_min - previous_x_max > -7 \
                and x_max > x_mid:
                result['deffensive_team']['heroes'][count_deffensive]['power'] = previous_pwr+pwr
                count_deffensive=count_deffensive+1
                previous_x_max = 0
                previous_pwr = ""
            elif previous_pwr != "" and previous_x_max <= x_mid and int(previous_pwr) > 100:
                result['offensive_team']['heroes'][count_offensive]['power'] = previous_pwr
                count_offensive=count_offensive+1
                previous_x_max = x_max
                previous_pwr = pwr
            elif previous_pwr != "" and previous_x_max > x_mid and int(previous_pwr) > 100:
                result['deffensive_team']['heroes'][count_deffensive]['power'] = previous_pwr
                count_deffensive=count_deffensive+1
                previous_x_max = x_max
                previous_pwr = pwr
            else:
                previous_x_max = x_max
                previous_pwr = pwr

        if count_offensive >= len(result['offensive_team']['heroes']) \
            and count_deffensive >= len(result['deffensive_team']['heroes']):
            break

def get_result(result, texts, team):
    i = team_jump(texts, team)

    i = jump(texts, ['Victory', 'Defeat'], i-2)
    
    # Read the previous block
    previous_block = readblock(texts[i-2], texts[i-1])
    result[team]['result'] = previous_block['text']


def compute_team_power(result, team):
    pwr = 0
    for hero in result[team]['heroes']:
        pwr = pwr + int(hero['power'])
    
    result[team]['power'] = int(pwr / 1000)

def compute_team_index(result, team):
    index = ""
    for hero_pos in heroes_position:
        for hero in result[team]['heroes']:
            if hero['name'] == hero_pos:
                index = index + ' ' + hero_pos
    result[team]['index'] = index


def get_x_mid(result, texts):
    l_hero = result['offensive_team']['heroes'][0]['name']
    r_hero = result['deffensive_team']['heroes'][0]['name']

    l_hero_block = get_block(texts, l_hero)
    r_hero_block = get_block(texts, r_hero)

    l_max_bound = l_hero_block['bounds'][2]
    r_max_bound = r_hero_block['bounds'][0]

    return int((int(l_max_bound) + int(r_max_bound)) / 2)


def get_block(texts, search_token, i=0):
    '''
    Get block from a seach token
    '''
    while i < len(texts):
        block = readblock(texts[i], texts[i+1])
        i=i+2

        if block['text'].startswith(search_token):
            return block
    return None

def team_jump(texts, team):
    i = jump(texts, ['Victory', 'Defeat'], 0)
    if team == 'deffensive_team':
        i = jump(texts, ['Damage'], i)
    return i

def jump(texts, search_tokens, i):
    '''
    Jump after the first search_token found
    '''
    while i < len(texts):
        text = readblock(texts[i], texts[i+1])['text']
        i=i+2

        found = False
        for token in search_tokens:
            if text.startswith(token):
                found = True
                break
        if found:
            break
    return i

# format a line
def readblock(line_text,line_bounds):
    text = '{}'.format(line_text).replace('text:', '').replace('\n', '')
    bounds = '{}'.format(line_bounds).replace('bounds:', '').replace('\n', '')
    return { 'text': text, 'bounds': bounds.split(',') }
