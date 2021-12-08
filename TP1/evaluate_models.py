import os
import numpy as np
from gensim.models import Word2Vec
from datetime import datetime

DATA_VALIDATION_PATH = 'data/questions-words.txt'
class question_word:
    def __init__(self, line):
        self.w1 = line.split(' ')[0].lower()
        self.w2 = line.split(' ')[1].lower()
        self.w3 = line.split(' ')[2].lower()
        self.match = line.split(' ')[3].replace('\n','').lower()

def get_error_question_words(model, words, vocab):
    w_error = []
    count_not_in_vocab = 0
    
    for question in words:
        try:
            result = model.wv.most_similar(positive=[question.w1, question.w2], negative=[question.w3], topn=10)   
            nearest_word = result[0]
            
            if nearest_word[0] != question.match:
                w_error.append(model.wv.similarity(nearest_word[0], question.match))
            else:
                w_error.append(0)
        except:
            w_error.append(1)
            count_not_in_vocab += 1
            
    mean = np.average(w_error)
    std = np.std(w_error)
    var = np.var(w_error)
    
    return mean, std, var, count_not_in_vocab

def run():
    with open(DATA_VALIDATION_PATH, 'r') as file:
        all_lines = file.readlines()
        
    words_to_evaluate = [question_word(ln) for ln in all_lines if ':' not in ln]

    #GET MODELS 
    v_files_names = []
    for file in os.listdir('saved_models/models'):
        if file.endswith('.model'):
            v_files_names.append(file)
            print(file)
    
    #WRITING FINAL FILE 
    with open('saved_models/models_values.csv', 'w') as rfile:
        count = 1
        rfile.write('model,mean,std,var,num_words_miss\n')

    for file in v_files_names:
        time = datetime.now().strftime("%H:%M:%S")
        print(file, ' - {0}/{1} - {2}'.format(count, len(v_files_names), time))

        w2v_model = Word2Vec.load('saved_models/{0}'.format(file))
        mean_error, std_error, std_var, w_not_vocab = get_error_question_words(w2v_model, words_to_evaluate, w2v_model.wv)
        del w2v_model

        with open('saved_models/models_values.csv', 'a') as rfile:
            rfile.write('{0},{1},{2},{3},{4}\n'.format(file, mean_error, std_error, std_var, w_not_vocab))
        
        print(mean_error, std_error, std_var, w_not_vocab, '\n')
        count += 1
        #exit()

run()