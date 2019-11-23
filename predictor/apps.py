import datetime
import json
import uuid

from pymongo import MongoClient
from django.apps import AppConfig
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from fastai.text import untar_data, load_data, URLs, AWD_LSTM, text_classifier_learner


class PredictorConfig(AppConfig):
    name = 'predictor'
    verbose_name = 'Sentiment predictor'


bs = 12
path = untar_data(URLs.IMDB)
data_clas = load_data(path, 'data_clas.pkl', bs=bs)
learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
learn.load_encoder('fine_tuned_enc')
learn.load('fourth')

password = 'rAL7TKvq6G6HD3kG'
client = MongoClient("mongodb+srv://wenti:{}@cluster0-rj4l5.gcp.mongodb.net/test?retryWrites=true&w=majority&ssl=true"
                     "&ssl_cert_reqs=CERT_NONE".format(password))
db = client.test
predictions, users = db.predictions, db.users


@csrf_exempt
def predict(req: HttpRequest):
    # Validate request
    if req.method == 'OPTIONS':
        res = HttpResponse()
        res['Allow'] = "['POST', 'OPTIONS']"
        return res

    elif req.method != 'POST':
        return HttpResponseNotAllowed(['POST', 'OPTIONS'])

    # Parse request body
    props = json.loads(req.body.decode('utf-8'))
    if len(props) != 1 or 'text' not in props:
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')

    # Parse request
    user_id = req.COOKIES.get('user_id');
    text = props.get('text')

    # Generate Prediction
    res_json = dict()
    res_json['prediction_id'] = str(uuid.uuid4())
    res_json['user_id'] = user_id
    res_json['text'] = text
    res_json['is_positive'] = True if str(learn.predict(text)[0]) == 'pos' else False
    # Time
    time = datetime.datetime.now()
    res_json['time_date'] = "{}-{}-{}T{}:{}:{}Z" \
        .format(time.year, time.month, time.day, time.hour, time.minute, time.second)
    res_json['object'] = 'prediction'

    # Create prediction document in DB
    predictions.insert_one({
        "prediction_id": res_json['prediction_id'],
        "user_id": user_id,
        "text": text,
        "is_positive": res_json['is_positive'],
        "time_date": time,
        "object": "prediction"
    })

    if user_id:
        # Add prediction to users
        add_prediction_to_user(user_id, res_json['prediction_id'])

    res = HttpResponse(json.dumps(res_json), content_type='application/json')
    res["Access-Control-Allow-Origin"] = "*"
    res['Access-Control-Allow-Methods'] = "'POST', 'OPTIONS']"
    return res


def add_prediction_to_user(user_id: str, prediction_id: str):
    users.insert_one(
        {'user_id': user_id},
        {'$push': {'prediction_ids': prediction_id}}
    )
