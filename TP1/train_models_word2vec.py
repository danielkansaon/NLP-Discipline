
from gensim.models import Word2Vec
from nltk.corpus import stopwords
import gensim.downloader as api
from nltk.tokenize import word_tokenize
import logging
from multiprocessing import cpu_count
import string
from datetime import datetime

# Declaração
STOP_WORDS = stopwords.words('english')
PUNCTUATION = ['!', '"', '#', '$', '%', '&', '\/', '(', ')', '*', '+', ',', '-', '.',
                '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~']

##logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def clean_text(v_text):
        # LOWER CASE
        v_text = [word.lower() for word in v_text]  
        # REMOVE STOPWORDS
        v_text = [word for word in v_text if word not in STOP_WORDS]
        # REMOVE PUNCTUATION
        v_text = [word for word in v_text if word not in PUNCTUATION]
        # REMOVE WHITE SPACES
        v_text = [word for word in v_text if word.strip() != '']

        return v_text

def train_all_models():  
    dataset = api.load("text8")

    DATA_ALL = []
    for word in dataset:
        DATA_ALL.append(clean_text(word))

    DATA_1 = DATA_ALL[:851]
    DATA_2 = DATA_ALL[851:]

    dim_params = [100,300,500]
    wind_params = [2,4,6,8,10]
    ep_params = [5, 10, 15, 20]

    all_tests = {
        '100-2-5': [0,0,0],
        '300-2-5': [1,0,0],
        '500-2-5': [2,0,0],
        '100-4-5': [0,1,0],
        '100-6-5': [0,2,0],
        '100-8-5': [0,3,0],
        '100-10-5': [0,4,0],
        '300-4-5': [1,1,0],
        '300-6-5': [1,2,0],
        '300-8-5': [1,3,0],
        '300-10-5': [1,4,0],
        '500-4-5': [2,1,0],
        '500-6-5': [2,2,0],
        '500-8-5': [2,3,0],
        '500-10-5': [2,4,0],
        #epochs
        '100-2-10': [0,0,1],
        '300-2-10': [1,0,1],
        '500-2-10': [2,0,1],
        '100-4-10': [0,1,1],
        '100-6-10': [0,2,1],
        '100-8-10': [0,3,1],
        '100-10-10': [0,4,1],
        '300-4-10': [1,1,1],
        '300-6-10': [1,2,1],
        '300-8-10': [1,3,1],
        '300-10-10': [1,4,1],
        '500-4-10': [2,1,1],
        '500-6-10': [2,2,1],
        '500-8-10': [2,3,1],
        '500-10-10': [2,4,1],
        #epochs
        '100-2-15': [0,0,2],
        '300-2-15': [1,0,2],
        '500-2-15': [2,0,2],
        '100-4-15': [0,1,2],
        '100-6-15': [0,2,2],
        '100-8-15': [0,3,2],
        '100-10-15': [0,4,2],
        '300-4-15': [1,1,2],
        '300-6-15': [1,2,2],
        '300-8-15': [1,3,2],
        '300-10-15': [1,4,2],
        '500-4-15': [2,1,2],
        '500-6-15': [2,2,2],
        '500-8-15': [2,3,2],
        '500-10-15': [2,4,2],
        #epochs
        '100-2-20': [0,0,3],
        '300-2-20': [1,0,3],
        '500-2-20': [2,0,3],
        '100-4-20': [0,1,3],
        '100-6-20': [0,2,3],
        '100-8-20': [0,3,3],
        '100-10-20': [0,4,3],
        '300-4-20': [1,1,3],
        '300-6-20': [1,2,3],
        '300-8-20': [1,3,3],
        '300-10-20': [1,4,3],
        '500-4-20': [2,1,3],
        '500-6-20': [2,2,3],
        '500-8-20': [2,3,3],
        '500-10-20': [2,4,3]
    }

    for d in [0,1,2]:
        data_sentences = DATA_1 if d == 0 else DATA_2 if d == 1 else DATA_ALL
        dataset_name = 'data1' if d == 0 else 'data2' if d == 1 else 'all_data'

        #CBOW
        count = 1
        for key, value in all_tests.items():
            time = datetime.now().strftime("%H:%M:%S")
            print('{0}/3 - CBOW training - {1}/{2} - {3} \n'. format(d+1, count, len(all_tests), time))

            w2v_model = Word2Vec(data_sentences,
                                min_count=1,
                                sg = 0, #skip-gram or cbow
                                window = wind_params[value[1]], #window size
                                vector_size = dim_params[value[0]], #dimensionality
                                hs = 0, #use negative sampling
                                negative = 5, #number sampling
                                epochs = ep_params[value[2]],
                                workers=cpu_count())

            w2v_model.save("saved_models/models/{0}-cbow-{1}.model".format(dataset_name, key))
            del w2v_model

            count += 1

        #SKIP-GRAM
        count = 1
        for key, value in all_tests.items():
            time = datetime.now().strftime("%H:%M:%S")
            print('{0}/3 - SKIP-GRAM training - {1}/{2} - {3} \n'. format(d+1, count, len(all_tests), time))
            w2v_model = Word2Vec(data_sentences,
                                min_count=1,
                                sg = 0, #skip-gram or cbow
                                window = wind_params[value[1]], #window size
                                vector_size = dim_params[value[0]], #dimensionality
                                hs = 0, #use negative sampling
                                negative = 5, #number sampling
                                epochs = ep_params[value[2]],
                                workers=cpu_count())

            w2v_model.save("saved_models/models/{0}-skip_gram-{1}.model".format(dataset_name, key))
            del w2v_model
            count += 1
