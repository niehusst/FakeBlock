# Import tensorflow
import tensorflow as tf
import keras.backend as K

# Helper libraries
import math
import numpy as np
import os
import sys
import time

# Imports for dataset manipulation
from sklearn.model_selection import train_test_split

# Improve progress bar display
import tqdm
import tqdm.auto
tqdm.tqdm = tqdm.auto.tqdm

tf.enable_eager_execution() #comment this out if causing errors
tf.logging.set_verbosity(tf.logging.DEBUG)



###             SET MODEL CONFIGURATIONS             ###
# Data Loading
CSV_PATH = 'label_data/CCC_clean.csv'
DATA_BASE_PATH = 'data/'
test_size_percent = 0.50 #percent of total data reserved for testing

# Loss
lambda_coord = 5
epsilon = 0.00001

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
# zip all points for each image label together into a tuple 
points = zip(data_frame['start_x'], data_frame['start_y'], \
                       data_frame['end_x'], data_frame['end_y'])
img_paths = data_frame['imgPath']



# apply preprocessing functions with map

# reshape input data ?

# split the preprocessed data into train and test
train_imgs, test_imgs, train_points, test_points = \
  train_test_split(imgs, points, test_size=test_size_percent, random_state=42)

num_train_examples = len(train_imgs)
num_test_examples = len(test_imgs)


"""
Create generator for feeding the training data to the model
in batches?
"""



###            DEFINITION OF MODEL SHAPE             ###
"""
Model definition TODO: ....

most fb posts wont be longer than 200 chars???
"""
model = tf.keras.Sequential([

    tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)
    # 1 output: predict classify input as fake or not
])


# small step size works best
model.compile(optimizer=tf.keras.optimizers.Adam(lr=step_size), #'rmsprop'
              loss='binary_crossentropy',
              metrics=['accuracy','mse'])

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
model.fit_generator(generator.flow(train_imgs, train_points, batch_size=BATCH_SIZE),
                        callbacks=callbacks, epochs=num_epochs,
                        steps_per_epoch=(num_train_examples // BATCH_SIZE))



###                 EVALUATE THE MODEL               ###

# evaluate the accuracy of the trained model using the test dataset
metrics = model.evaluate(test_imgs, test_points)
print("Final loss:{}\nFinal accuracy:{}".format(metrics[0], metrics[1]))



###                 SAVING THE MODEL                 ###
# save the model so that it can be loaded without training later

# serialize model to JSON
model_json = model.to_json()
with open(shape_path, "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights(weight_path)
print("Saved model to disk")

