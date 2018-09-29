from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch(timeout=10,sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=60,sniff_timeout=10,max_retries=10)

request_body = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    'mappings': {
        'tweet': {
                'author': {'type': 'string'},
                'text': {'type': 'string'},
                'timestamp': {'type': 'string'},
            }
    }
}

##es.indices.delete(index='test-index')
es.indices.delete(index='user')
##es.indices.refresh()

##print("creating 'user' index...")
##es.indices.create(index='test-index', body=request_body)
'''
doc = {
    'author': 'Kerninghan & Ritchie',
    'text': 'Know your C',
    'timestamp': '192-002002',
}


es.index(index="test-index", doc_type="tweet", body={"author": "data", "timestamp": str(datetime.now())})



res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
print(res['result'])

res = es.get(index="test-index", doc_type='tweet', id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

'''