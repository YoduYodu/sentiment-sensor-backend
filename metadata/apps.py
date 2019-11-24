import json
from django.apps import AppConfig
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient


class MetadataConfig(AppConfig):
    name = 'metadata'


password = 'rAL7TKvq6G6HD3kG'
client = MongoClient("mongodb+srv://wenti:{}@cluster0-rj4l5.gcp.mongodb.net/test?retryWrites=true&w=majority&ssl=true"
                     "&ssl_cert_reqs=CERT_NONE".format(password))
db = client.test
metadata = db.metadata


@csrf_exempt
def metadata(req: HttpRequest):
    md = metadata.find_one(
        {'id': 'metadata'}
    )
    del md['_id']
    response = HttpResponse(json.dumps(md), content_type='application/json')
    response["Access-Control-Allow-Origin"] = "*"
    response['Access-Control-Allow-Methods'] = "'POST', 'OPTIONS', 'GET']"
    return response


