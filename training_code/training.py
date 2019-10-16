# -*- coding: utf-8 -*-

# Commented out IPython magic to ensure Python compatibility.
# %reload_ext autoreload
# %autoreload 2
# %matplotlib inline

from fastai.text import *

# Get the dataset
bs=48
path = untar_data(URLs.IMDB)
data_lm = (TextList.from_folder(path)
            .filter_by_folder(include=['train', 'test', 'unsup'])
            .split_by_rand_pct(0.1)
            .label_for_lm()
            .databunch(bs=bs))
data_lm.save('data_lm.pkl')
data_lm = load_data(path, 'data_lm.pkl', bs=bs)

# Train model
learn = language_model_learner(data_lm, AWD_LSTM, drop_mult=0.3)
learn.fit_one_cycle(1, 1e-2, moms=(0.8,0.7))
learn.save('fit_head')
learn.load('fit_head');

# Unfreeze and fine-tune and re-train it
learn.unfreeze()
learn.fit_one_cycle(10, 1e-3, moms=(0.8,0.7))
learn.save('fine_tuned')
learn.load('fine_tuned');

learn.save_encoder('fine_tuned_enc')  # Save the encoder here


# Train classifier here (what we need)
path = untar_data(URLs.IMDB)
data_clas = (TextList.from_folder(path, vocab=data_lm.vocab)
             .split_by_folder(valid='test')
             .label_from_folder(classes=['neg', 'pos'])
             .databunch(bs=bs))

data_clas.save('data_clas.pkl')
data_clas = load_data(path, 'data_clas.pkl', bs=bs)
learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
learn.load_encoder('fine_tuned_enc')

# Train first layer
learn.fit_one_cycle(1, 2e-2, moms=(0.8,0.7))
learn.save('first')

# Train second layer
learn.load('first');
learn.freeze_to(-2)
learn.fit_one_cycle(1, slice(1e-2/(2.6**4),1e-2), moms=(0.8,0.7))
learn.save('second')
learn.load('second');

# Train third layer
learn.freeze_to(-3)
learn.fit_one_cycle(1, slice(5e-3/(2.6**4),5e-3), moms=(0.8,0.7))
learn.save('third')

# Train fourth layer
learn.load('third');
learn.unfreeze()
learn.fit_one_cycle(2, slice(1e-3/(2.6**4),1e-3), moms=(0.8,0.7))

# 
learn.predict("I really loved that movie, it was awesome!")