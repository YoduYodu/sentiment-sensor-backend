from django.apps import AppConfig
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from fastai.text import untar_data, load_data, URLs, AWD_LSTM, text_classifier_learner
import uuid, datetime, json
from django.views.decorators.csrf import csrf_exempt


class PredictorConfig(AppConfig):
    name = 'predictor'
    verbose_name = 'Sentiment predictor'


bs = 12
path = untar_data(URLs.IMDB)
data_clas = load_data(path, 'data_clas.pkl', bs=bs)
learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
learn.load_encoder('fine_tuned_enc')
learn.load('fourth')


@csrf_exempt
def predict(req):
    # Validate request
    if req.method == 'OPTIONS':
        res = HttpResponse()
        res['Allow'] = "['POST', 'OPTIONS']"
        return res

    elif req.method != 'POST':
        return HttpResponseNotAllowed(['POST', 'OPTIONS'])

    # Parse request body
    props = json.loads(req.body.decode('utf-8'))
    if len(props) != 2 or 'user_id' not in props or 'text' not in props:
        return HttpResponseBadRequest('Bad Request', content_type='text/plain')

    # Parse request
    user_id = props.get('user_id')
    text = props.get('text')

    # Generate Predictioncsrf
    res_json = dict()
    res_json['uuid'] = str(uuid.uuid4())
    res_json['user_id'] = user_id
    res_json['text'] = text
    res_json['is_positive'] = True if str(learn.predict(text)[0]) == 'pos' else False
    # Time
    time = datetime.datetime.now()
    res_json['time_date'] = "{}-{}-{}T{}:{}:{}Z"\
        .format(time.year, time.month, time.day, time.hour, time.minute, time.second)
    res_json['object'] = 'prediction'

    res = HttpResponse(json.dumps(res_json), content_type='application/json')
    res["Access-Control-Allow-Origin"] = "*"
    res['Access-Control-Allow-Methods'] = "'POST', 'OPTIONS']"
    return res




