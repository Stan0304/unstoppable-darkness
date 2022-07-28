import google.cloud.bigquery.dbapi as bq
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

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

delete_collection(battles_db,100)
