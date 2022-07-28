from google.cloud import firestore
from pprint import pprint

db = firestore.Client()
battles_db = db.collection(u'battles')

#print("query1:")
#battles = battles_db.where(u'poster', u'==', u'stan').get()
#for battle in battles:
#    pprint(battle.to_dict()['image_url'])

# ;Astaroth;Krista;Celeste;Jorgen;Lars;

print("query2:")
battles = battles_db.where(
    u'offensive_team.index', u'array_contains', ['Astaroth', 'Krista']).get()
for battle in battles:
    pprint(battle.to_dict()['image_url'])
