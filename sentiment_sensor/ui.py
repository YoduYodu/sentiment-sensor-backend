from fastai.text import *

bs=12
path = untar_data(URLs.IMDB)
data_clas = load_data(path, 'data_clas.pkl', bs=bs)
learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
learn.load_encoder('fine_tuned_enc')
learn.load('second')
print(learn.predict('This movie is so great!'))

while True:
    try:
        text_review = input('Input a review you\'d like to review\n')
    except Exception:
        continue
    # print(str(learn.predict(text_review)[0]))
    if str(learn.predict(text_review)[0]) == 'pos':
        print('Positive review')
    else:
        print('Negative review')
