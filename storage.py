from google.cloud import bigquery
from google.cloud import firestore
from pprint import pprint

# Firestore - store battles
dbdoc_client = firestore.Client()
battles_db = dbdoc_client.collection(u'battles')

# Bigquery - index to search battles
dbidx_client = bigquery.Client()
dbidx_ds_ref = dbidx_client.dataset('hw_db_index')
dbidx_table_ref = dbidx_ds_ref.table('battles')
dbidx_table = dbidx_client.get_table(dbidx_table_ref)

def store_battle(result):
    # Check if the battle already indexed by bigquery
    query = dbidx_client.query('SELECT record_id FROM `credible-market-195106.hw_db_index.battles` WHERE unik="{}" LIMIT 1'.format(result['index']['unik']))
    results = query.result() 
    for result in results:
        raise Exception('This battle has already been processed with RecordId={}'.format(result.record_id))

    # Insert the battle as document
    battle_ref = battles_db.add(result['battle'])[1]

    # Index the battle with bigquery
    result['index']['record_id'] = battle_ref.id
    result['index']['defensive_player'] = result['battle']['defensive_team']['player']
    result['index']['offensive_player'] = result['battle']['offensive_team']['player']
    errors = dbidx_client.insert_rows(dbidx_table, [result['index']])
    
    if errors != []:
        print("Insert errors:", errors)
        raise Exception('Battle indexation failed the battle')
    

    return battle_ref.id


def get_battle(record_id):
    result = {}
    # Get the index infos
    query = dbidx_client.query('SELECT * FROM `credible-market-195106.hw_db_index.battles` WHERE record_id="{}" LIMIT 1'.format(record_id))
    indexes = query.result() 

    if indexes.total_rows == 0:
        raise Exception('No battle found with those criteria')

    for index in indexes:
        result['index'] = {
            'record_id': index.record_id,
            'offensive_team': index.offensive_team,
            'defensive_team': index.defensive_team,
            'unik': index.unik,
            'type': index.type,
            'offensive_player': index.offensive_player,
            'defensive_player': index.defensive_player
        }

    # Get the battle
    result['battle'] = battles_db.document(record_id).get().to_dict()
    
    return result


def query(q_ids, q_player, q_heroes):
    result = {}

    # Get the index infos
    q_battle_from = 'SELECT * FROM `credible-market-195106.hw_db_index.battles`'
    
    q_battle_id = ' record_id IN ("{}")'.format( '","'.join(q_ids))
    q_battle_player = ' ( offensive_player LIKE "%{}%" OR  defensive_player LIKE "%{}%")'.format(q_player, q_player)
    q_battle_heroes = ' ( REGEXP_CONTAINS(offensive_team, r"{}") OR REGEXP_CONTAINS(defensive_team, r"{}") )'.format(q_heroes, q_heroes)

    str_query = q_battle_from + ' WHERE '

    add_end = False
    if len(q_ids) > 0:
        str_query += q_battle_id
        add_end = True
    
    if q_player != "" and add_end:
        str_query += ' AND ' + q_player
    elif q_player != "":
        str_query += q_player
        add_end = True

    if q_heroes != ".*" and add_end:
        str_query += ' AND ' + q_battle_heroes
    elif q_heroes != ".*":
        str_query += q_battle_heroes

    if len(q_ids) == 0 and q_heroes == ".*":
        raise Exception('Add at least heroes or ids to your search criteria')

    print("bigquery: "+str_query)
    query = dbidx_client.query(str_query)
    indexes = query.result()
    
    if indexes.total_rows == 0:
        raise Exception('No battle found with those criteria')

    for index in indexes:
        result['index'] = {
            'record_id': index.record_id,
            'offensive_team': index.offensive_team,
            'defensive_team': index.defensive_team,
            'unik': index.unik,
            'type': index.type,
            'offensive_player': index.offensive_player,
            'defensive_player': index.defensive_player
        }

    # Get the battle
    result['battle'] = battles_db.document(result['index']['record_id']).get().to_dict()
    
    return result

#pprint(get_battle('6pC8OGgwmHgShjveWJu3'))