from google.cloud import bigquery
from google.cloud import firestore
from pprint import pprint

# Firestore - store battles
dbdoc_client = firestore.Client()
battles_db = dbdoc_client.collection(u'battles')

# Bigquery - index to search battles
dbidx_client = bigquery.Client()
dbidx_ds_ref = dbidx_client.dataset('hw_db_index')
dbidx_table_ref = dbidx_ds_ref.table('index')
dbidx_table = dbidx_client.get_table(dbidx_table_ref)

def store_battle(result):
    # Check if the battle already indexed by bigquery
    query = dbidx_client.query('SELECT record_id FROM `credible-market-195106.hw_db_index.index` WHERE unik="{}" LIMIT 1'.format(result['index']['unik']))
    results = query.result() 
    for result in results:
        raise Exception('This battle has already been processed with RecordId={}'.format(result.record_id))

    battle_ref = battles_db.add(result)[1]

    # Index the battle with bigquery
    result['index']['record_id'] = battle_ref.id
    errors = dbidx_client.insert_rows(dbidx_table, [result['index']])
    assert errors == []

    return battle_ref.id

result={'offensive_team': {'heroes': [{'name': 'Krista', 'power': 103930}, {'name': 'Lars', 'power': 103667}, {'name': 'Jorgen', 'power': 103745}, {'name': 'Astaroth', 'power': 103873}, {'name': 'Celeste', 'power': 37786}], 'result': 'Victory', 'player': 'bbbbb1991', 'guild': 'Synergized Cookie', 'power': 453}, 'defensive_team': {'heroes': [{'name': 'Ishmael', 'power': 105754}, {'name': 'Sebastian', 'power': 85861}, {'name': 'Astaroth', 'power': 95125}, {'name': 'Martha', 'power': 74738}, {'name': 'Jorgen', 'power': 68086}], 'result': 'Defeat', 'player': 'butz +4', 'guild': 'Heroes of Tomorrow', 'power': 429}, 'record_id': 1, 'poster': 'stan', 'image_url': 'https://media.discordapp.net/attachments/795675024593125406/930837291709128854/IMG_0151.png?width=1343&height=621', 'index': { 'unik': 'c0c6d842e3cce1f0bd761e6b46fcabadfa83d723052bcc4d6b4ba021e91b10c', 'offensive_team': ';Astaroth;Krista;Celeste;Jorgen;Lars;', 'defensive_team': 'Astaroth;Ishmael;Sebastian;Jorgen;Martha;'}, 'type': 'arena'}
battle_id = store_battle(result)

print("Battle added")
print(battle_id)

exit(0)
