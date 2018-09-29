from flask import Flask, jsonify, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)

es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=10, sniff_on_start=True,
                   sniff_on_connection_fail=True, sniffer_timeout=60, sniff_timeout=10, max_retries=10)


@app.route('/user', methods=["POST"])
def adduser():
    '''
    API which adds a User to Elasticsearch and
    :return: added User json
    '''
    q = request.form.get("q")
    username = request.form.get("username").strip()
    email = request.form.get("email").strip()
    address = request.form.get("address").strip()
    birthdate = request.form.get("birthdate").strip()
    user = {
        'username': username.strip(),
        'email': email.strip(),
        'address': address.strip(),
        'birthdate': birthdate.strip(),
    }
    if username.strip() != "":
        es.index(index="user", doc_type="user", body=user)
        es.indices.refresh(index="user")
    return jsonify(user)


@app.route('/user', methods=["DELETE"])
def deluser():
    '''
    Delete any username which are empty (cleanup via Title click)
    :return:
    '''
    es.delete_by_query(index="user", doc_type="user",
                                 body={"query": {"bool": {
                                     "must_not": {
                                         "exists": {
                                             "field": "username"
                                         }
                                     }
                                 }
                                 }})
    es.indices.refresh(index="user")
    del_msg = es.delete_by_query(index="user", doc_type="user",
                                 body={"query": {
                                     "term": {
                                         "username": ""
                                     }
                                 }})
    es.indices.refresh(index="user")
    return jsonify(del_msg)


@app.route('/user', methods=["GET"])
def getuser():
    '''
    GET USER API
    Method: GET
    :return: a list of users
    '''
    resp = es.search(index="user", doc_type="user", size=50, body={"query": {"match_all": {}}})
    return jsonify(resp)


@app.route('/', methods=["GET", "POST"])
def listuser():
    '''
    Landing page with template Get and Post
    There are 2 forms - Add and Search
    Shows a Table of Users
    :return: Displays 50 Users, pagination to be done.
    '''
    q = request.form.get("q")
    username = request.form.get("username")
    email = request.form.get("email")
    address = request.form.get("address")
    birthdate = request.form.get("birthdate")
    if username is not None:
        user = {
            'username': username.strip(),
            'email': email.strip(),
            'address': address.strip(),
            'birthdate': birthdate.strip(),
        }

    if es.indices.exists(index="user"):
        es.indices.refresh(index="user")
    if not es.indices.exists(index="user"):
        createindexforuser()

    resp = es.search(index="user", doc_type="user", size=50, body={"query": {"match_all": {}}})
    if q is not None:
        resp = es.search(index="user", doc_type="user", size=50, body={"query": {"prefix": {"username": q}}})
        return render_template("index.html", title="{'Project' : 'Mapillary Automation test challenge'}", q=q,
                               response=resp)
    else:
        return render_template("index.html", title="{'Project' : 'Mapillary Automation test challenge'}", q='',
                               response=resp)


def createindexforuser():
    '''
    Creates an index "user" in elasticsearch with fields { username, email, address, birthdate }
    :return:
    '''
    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        'mappings': {
            'user': {
                'properties': {
                    'username': {'type': 'text'},
                    'email': {'type': 'text'},
                    'address': {'type': 'text'},
                    'birthdate': {'type': 'text'},
                }}}
    }
    print("creating 'user' index...")
    es.indices.refresh()
    es.indices.create(index='user', body=request_body)

'''
Start the Flash and UI template to show up on Port 9100
'''
if __name__ == "__main__":
    app.run(debug=True, port=9100)
