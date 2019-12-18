import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical


class PredictionModel(object):
	def __init__(self, shape_file, weights_file, tokenizer_file):
		#load up model
		self.model = self._load_model(shape_file, weights_file)
		with open(tokenizer_file, 'r') as json_fp:
			self.tokenizer = tokenizer_from_json(json_fp.read())
	
	def predict(self, text):
		"""
		use the loaded model to make binary predicttion on the
		truthyness of the input `text`
		TODO: check if text is english and dont run on it if it isnt?

		@param text - String, news title/fb post to evaluate
		@return - Float, a probability in the range of 0-1 where a
					prediction of 1 indicates FAKE and 0 is NOT FAKE
		"""
		return self.model.predict(self._process(text))[0][0]

	def _load_model(self, shape_file, weights_file):
		"""
		Load a tensorflow/keras model from `shape_file`, a JSON file that
		describes the shape of the model, and `weights_file`, and HDF5 file
		that describes the final neuron weights of a trained model.

		@param shape_file - String, path to a valid JSON file
		@param weights_file - String, path to a valid HDF5 weights file
		@return loaded_model - a fully trained tf/keras model
		"""
		print("Loading model from disk...", end="", flush=True)
		# load json and create model
		json_file = open(shape_file, 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		loaded_model = tf.keras.models.model_from_json(loaded_model_json)
		# load weights into new model
		loaded_model.load_weights(weights_file)
		print("Complete!")
		return loaded_model

	def _process(self, text):
		"""
		Process `text` so that it can be predicted on by the model.

		@param text - String, text to process for the classification model
		@return - Python list, a vector encoded array of positive integers
					that represent `text` in a way the model understandes
		"""
		MAX_SEQUENCE_LENGTH = 200
		# use trained tokenizer to convert to seqs
		sequences = self.tokenizer.texts_to_sequences([text])
		data = pad_sequences(sequences, 
							maxlen=MAX_SEQUENCE_LENGTH, 
							padding='pre', 
							truncating='pre')
		return data

#test model
"""
m = PredictionModel('trained_model/model_shape.json', 'trained_model/model_weights.h5', 'trained_model/tokenizer.json')
print(m.predict("Trump KILLS Hillary with shotgun on live TV!"))
print(m.predict("The earth is flat!"))
print(m.predict("Who even is this Bill Murray guy?? Anyone want to fill me in?"))
print(m.predict("Speaker of the house, Elizabeth Warren, calls vote on new Bill"))
"""