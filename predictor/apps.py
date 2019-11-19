from django.apps import AppConfig
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from fastai.text import untar_data, load_data, URLs, AWD_LSTM, text_classifier_learner
import uuid, datetime, json


class PredictorConfig(AppConfig):
    name = 'predictor'
    verbose_name = 'Sentiment predictor'

bs = 12
path = untar_data(URLs.IMDB)
data_clas = load_data(path, 'data_clas.pkl', bs=bs)
learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
learn.load_encoder('fine_tuned_enc')
learn.load('fourth')


def predict(req):
    # Validate request
    if req.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    elif len(req.GET) != 2 or 'user_id' not in req.GET or 'text' not in req.GET:
        return HttpResponseBadRequest('Bad Request')

    # Parse request
    props = req.GET
    user_id = props.get('user_id')
    text = props.get('text')

    # Generate Prediction
    res_json = dict()
    res_json['uuid'] = str(uuid.uuid4())
    res_json['user_id'] = user_id
    res_json['text'] = text
    res_json['is_positive'] = True if learn.predict(text)[0] is 'pos' else False

    # Time
    time = datetime.datetime.now()
    res_json['time_date'] = "{}-{}-{}T{}:{}:{}Z"\
        .format(time.year, time.month, time.day, time.hour, time.minute, time.second)
    res_json['object'] = 'prediction'

    return HttpResponse(json.dumps(res_json), content_type='application/json')




