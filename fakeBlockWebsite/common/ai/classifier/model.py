# Import tensorflow
import tensorflow as tf

# Helper libraries
import numpy as np
import os
import sys
import time

# Imports for dataset pre-processing
from sklearn.model_selection import train_test_split
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Improve training progress bar display
import tqdm
import tqdm.auto
tqdm.tqdm = tqdm.auto.tqdm


###             SET MODEL CONFIGURATIONS             ###
# Data Loading
CSV_PATH = 'data/fake_news_dataset.csv'
DATA_BASE_PATH = 'data/'
test_size_percent = 0.20

# Learning
step_size = 0.001
BATCH_SIZE = 32
num_epochs = 2  #TODO training caps out around 4 ephochs?

# Data info
MAX_SEQUENCE_LENGTH = 200  # max num words in typical FB post
MAX_NUM_WORDS = 25000      # max that embedder can learn
EMBEDDING_DIM = 300        # what GloVe uses

# Saving
shape_path = 'trained_model/model_shape.json'
weight_path = 'trained_model/model_weights.h5'
tokenizer_path = 'trained_model/tokenizer.json'

# TensorBoard 
tb_graph = False
tb_update_freq = 'batch'


            
###         GET THE DATASET AND PREPROCESS IT        ###

print("Loading and processing data\n") 

data_frame = pd.read_csv(CSV_PATH)

"""TODO: understand what is happeingin here. Could other/extra processing improve results?
Process the text input (news titles) into tokenized number
sequences that the model can more easily learn/be run on.
""" 
news_titles = data_frame['title']
news_fakeness = data_frame['fake']

# apply preprocessing
tokenizer = Tokenizer(num_words=MAX_NUM_WORDS) 
tokenizer.fit_on_texts(news_titles)
# save the tokenizer for use later
with fp as open(tokenizer_path, 'w'):
    fp.write(tokenizer.to_json())

sequences = tokenizer.texts_to_sequences(news_titles)

word_index = tokenizer.word_index
num_words = min(MAX_NUM_WORDS, len(word_index)) + 1
data = pad_sequences(sequences, 
                     maxlen=MAX_SEQUENCE_LENGTH, 
                     padding='pre', 
                     truncating='pre')


# split the preprocessed data into train and test
train_titles, test_titles, train_fake, test_fake = \
  train_test_split(data, news_fakeness, test_size=test_size_percent, random_state=42)

num_train_examples = len(train_titles)
num_test_examples = len(test_titles)
steps_in_epoch = (num_train_examples // BATCH_SIZE)


"""
Define generator function for feeding the training data to the model
in batches
"""
def load_data(train_data, train_labels, idx, batch_size):
    start = idx * batch_size
    end = start + batch_size
    x = np.array(train_data[start:end])
    y = np.array(train_labels[start:end])
    return (x, y)

def generator(train_data, train_labels, batch_size, steps):
    idx=1
    while True: 
        yield load_data(train_data, train_labels, idx-1, batch_size)
        
        if idx < steps:
            idx += 1
        else:
            #start new epoch
            idx = 1


print("Data processing complete\n")

###            DEFINITION OF MODEL SHAPE             ###
"""
#TODO find optimal hyper params. grid search? k-folds cross-validation?? random search?
#TODO add more hidden layers? more complex network better able to approximate this function space?

I could make a classification model, but given the ambiguity of the
problem at hand, a prediction (regression) model would likely be better
(response can be threshholded after the fact)

TODO: compare the many diff models
git DNN { 
    #seems to be overfitting; test acc doesnt get much better after more than 1 epoch
    Final (testing) accuracy: 0.7841007709503174
    Final AUC: 0.863892138004303
}
SVM {
    Training Accuracy: 88.02%
    Testing Accuracy: 77.41%
}
Naive Bayes { #note that these may be unreliable metrics, although it appears to do reasonably better than random/constant guessing
    Training Accuracy: 86.64%
    Testing Accuracy: 77.93%
}
LSTM?
Attention?

"""
model = tf.keras.Sequential([
    # part 1: word and sequence processing
    tf.keras.layers.Embedding(num_words,
                         EMBEDDING_DIM, 
                         input_length=MAX_SEQUENCE_LENGTH,
                         trainable=True),
    tf.keras.layers.Conv1D(128, 5, activation='relu'),
    tf.keras.layers.GlobalMaxPooling1D(),
        
    # part 2: classification
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])


# build the model
model.compile(optimizer=tf.keras.optimizers.Adam(lr=step_size),
              loss='binary_crossentropy',
              metrics=['accuracy',
                        'mse', 
                        tf.keras.metrics.AUC(), 
                        tf.keras.metrics.Recall(), 
                        tf.keras.metrics.Precision()])

#print(model.summary()) #see the shape of the model


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
model.fit_generator(generator(train_titles, train_fake, batch_size=BATCH_SIZE, steps=steps_in_epoch),
    callbacks=callbacks, 
    epochs=num_epochs,
    steps_per_epoch=steps_in_epoch)



###                 EVALUATE THE MODEL               ###

# evaluate the accuracy of the trained model using the test dataset
metrics = model.evaluate(test_titles, test_fake)
print("Final loss: {}\nFinal accuracy: {}\nFinal AUC: {}".format(metrics[0], metrics[1], metrics[3]))


#TODO: analyze which values the model misses most
model.evaluate(test_titles[0], test_fake[0], batch_size=1)


###                 SAVING THE MODEL                 ###
# save the model so that it can be loaded without training later

# serialize model to JSON
model_json = model.to_json()
with open(shape_path, "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights(weight_path)
print("Saved model to disk")

