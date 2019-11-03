from django.apps import AppConfig
from django.http import HttpRequest, HttpResponse
from fastai.text import untar_data, load_data, URLs, AWD_LSTM, text_classifier_learner

bs=12
path = untar_data(URLs.IMDB)
data_clas = load_data(path, 'data_clas.pkl', bs=bs)
learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
learn.load_encoder('fine_tuned_enc')
learn.load('fourth')


class PredictorConfig(AppConfig):
    name = 'predictor'


def predict(request: HttpRequest):
    # print(AppConfig.path)
    return HttpResponse(learn.predict(request.GET.get('text', 'No text input found'))[0])
