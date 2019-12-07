# Import tensorflow
import tensorflow as tf

# Helper libraries
import numpy as np
import os
import sys
import time

# Imports for dataset pre-processing
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer #FOR naive bayes. TODO remove
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

# Improve training progress bar display
import tqdm
import tqdm.auto
tqdm.tqdm = tqdm.auto.tqdm

#svm imports
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
import nltk
nltk.download('wordnet')
nltk.download('stopwords')


###             SET MODEL CONFIGURATIONS             ###
# Data Loading
CSV_PATH = 'data/fake_news_dataset.csv'
DATA_BASE_PATH = 'data/'
test_size_percent = 0.20 #percent of total data reserved for testing

# Learning
step_size = 0.001
BATCH_SIZE = 32
num_epochs = 1

# Saving
shape_path = 'trained_model/model_shape.json'
weight_path = 'trained_model/model_weights.h5'

# TensorBoard 
tb_graph = False
tb_update_freq = 'batch'


            
###         GET THE DATASET AND PREPROCESS IT        ###

print("Loading and processing data\n") 

data_frame = pd.read_csv(CSV_PATH)

"""
Construct numpy ndarrays from the loaded csv to use as training
and testing datasets.
""" 
news_titles = [word_tokenize(str(string).lower()) for string in data_frame['title']] #lowering may destroy valuable context data from all caps words?
news_fakeness = data_frame['fake']

# apply preprocessing functions with map
#svm preproc
tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

for index,entry in enumerate(news_titles):
    # Declaring Empty List to store the words that follow the rules for this step
    Final_words = []
    # Initializing WordNetLemmatizer()
    word_Lemmatized = WordNetLemmatizer()
    # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
    for word, tag in pos_tag(entry):
        # Below condition is to check for Stop words and consider only alphabets
        if word not in stopwords.words('english') and word.isalpha():
            word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
            Final_words.append(word_Final)
    # The final processed set of words for each iteration will be stored in 'text_final'
    data_frame.loc[index,'text_final'] = str(Final_words)


# reshape input data TODO?

# split the preprocessed data into train and test
train_titles, test_titles, train_fake, test_fake = \
  train_test_split(data_frame['text_final'], news_fakeness, test_size=test_size_percent, random_state=42)

num_train_examples = len(train_titles)
num_test_examples = len(test_titles)

#encode for SVM
encoder = LabelEncoder()
train_fake = encoder.fit_transform(train_fake)
test_fake = encoder.fit_transform(test_fake)

Tfidf_vect = TfidfVectorizer(max_features=5000)
Tfidf_vect.fit(data_frame['text_final'])
print(train_titles)
Train_titles_Tfidf = Tfidf_vect.transform(train_titles)
Test_titles_Tfidf = Tfidf_vect.transform(test_titles)
#print(Tfidf_vect.vocabulary_)
"""
TODO: Create generator for feeding the training data to the model
in batches?
"""



###            DEFINITION OF MODEL SHAPE             ###
"""
Naive Bayes and SVM show decent results, but Deep learning models
take the cake performance-wise (usually?).

I could make a classification model, but given the ambiguity of the
problem at hand, a prediction (regression) model would likely be better
(response can be threshholded after the fact)

TODO: compare the many diff models
git DNN
SVM {
    Training Accuracy: 88.02%
    Testing Accuracy: 77.41%
}
Naive Bayes { #note that these may be unreliable metrics, although it appears to do reasonably better than random/constant guessing
    Training Accuracy: 86.64%
    Testing Accuracy: 77.93%
}
LSTM?


Data needs pre-processing?
CLASSIC TYPES OF PREPROC
-> convert words to numbers + embedding vector conversion
(manually required??)
-> TFIDF
-> word2vec

https://www.toptal.com/machine-learning/nlp-tutorial-text-classification
embedding
conv1d
flatten
dense
// ^ this performed worse than SVM




Model definition TODO: ....

most fb posts wont be longer than 200 chars???
"""

# Attempt at SVM model

def evaluate_model(predict_fun, X_train, y_train, X_test, y_test):
    '''
    evaluate the model, both training and testing errors are reported
    '''
    # training error
    y_predict_train = predict_fun(X_train)
    train_acc = accuracy_score(y_train,y_predict_train)
    
    # testing error
    y_predict_test = predict_fun(X_test)
    test_acc = accuracy_score(y_test,y_predict_test)
    
    return train_acc, test_acc


#get generic svm model
model = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
model.fit(Train_titles_Tfidf,train_fake)


# evaluate model
train_acc, test_acc = evaluate_model(model.predict, Train_titles_Tfidf, train_fake, Test_titles_Tfidf, test_fake)
print("Training Accuracy: {:.2f}%".format(train_acc*100))
print("Testing Accuracy: {:.2f}%".format(test_acc*100))


"""
model = tf.keras.Sequential([

    tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)
    # 1 output: predict classify input as fake or not
])


# small step size works best
model.compile(optimizer=tf.keras.optimizers.Adam(lr=step_size), #'rmsprop'
              loss='binary_crossentropy',
              metrics=['accuracy',
                        'mse', 
                        tf.keras.metrics.AUC(), 
                        tf.keras.metrics.Recall(), 
                        tf.keras.metrics.Precision()])

print(model.summary()) #see the shape of the model


###                   TRAIN THE MODEL                ###
callbacks = []

# use tensorboard to visualize training on localhost:6006. Call from terminal with:
#>tensorboard --logdir=/path/to/logs
callbacks.append(tf.keras.callbacks.TensorBoard(log_dir='tb_logs/{}'.format(time.time()),
                                                 write_graph=tb_graph,
                                                 batch_size=BATCH_SIZE,
                                                 update_freq=tb_update_freq))


print('Fitting the model\n')
# start training the model using the data generator and the configurations
# specified at the top of the file
model.fit(train_titles, train_fake, #TODO get rid of generator?
    batch_size=BATCH_SIZE,
    callbacks=callbacks, 
    epochs=num_epochs,
    steps_per_epoch=(num_train_examples // BATCH_SIZE))



###                 EVALUATE THE MODEL               ###

# evaluate the accuracy of the trained model using the test dataset
metrics = model.evaluate(test_titles, test_fake)
print("Final loss:{}\nFinal accuracy:{}\nFinal AUC:{}".format(metrics[0], metrics[1], metrics[3]))



###                 SAVING THE MODEL                 ###
# save the model so that it can be loaded without training later

# serialize model to JSON
model_json = model.to_json()
with open(shape_path, "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights(weight_path)
print("Saved model to disk")
"""
