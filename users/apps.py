import json
from django.apps import AppConfig
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient


class UsersConfig(AppConfig):
    name = 'users'


password = 'rAL7TKvq6G6HD3kG'
client = MongoClient("mongodb+srv://wenti:{}@cluster0-rj4l5.gcp.mongodb.net/test?retryWrites=true&w=majority&ssl=true"
                     "&ssl_cert_reqs=CERT_NONE".format(password))
db = client.test
users = db.users


@csrf_exempt
def users(req: HttpRequest):
    if req.method == 'GET':
        return do_get(req)

    elif req.method == 'POST':
        return do_post_add_new_user(req)


def do_get(req: HttpRequest):
    props = json.loads(req.body.decode('utf-8'))
    user = users.find_one(
        {'user_id': props.get('user_id')}
    )
    del user['_id']
    res = HttpResponse(json.dumps(user), content_type='application/json')
    res["Access-Control-Allow-Origin"] = "*"
    res['Access-Control-Allow-Methods'] = "'POST', 'OPTIONS', 'GET']"
    return res


def do_post_add_new_user(req):
    props = json.loads(req.body.decode('utf-8'))
    new_user = {
            'user_id': props.get('user_id'),
            'password': props.get('password'),
            'submissions': [],
            'total_submission': 0,
            'total_positive': 0,
            'total_negative': 0,
            'total_correct': 0,
            'total_incorrect': 0
    }

    users.insert_one(new_user)
    return new_user


def do_post_update_on_user(user_id, is_positive):
    users.update_one(
        {'user_id': user_id},
        {'$inc': {
            'user_submission': 1,
            'user_positive': 1 if is_positive else 0,
            'user_negative': 0 if is_positive else 1,
        }}
    )
