from rest_framework.response import Response
from rest_framework.views import APIView

from common.ai.determinators import FakeDeterminator



#path from where manage.py is
base_path = "common/ai/classifier/trained_model/"
shapef = base_path + "model_shape.json"
weightf = base_path + "model_weights.h5"
tokenf = base_path + "tokenizer.json"
thresh = 0.7
# get the singleton instance of FakeDeterminator class     TODO does it even need to be singleton??
determinator = FakeDeterminator(thresh, shapef, weightf, tokenf)


# URL /api/fake
class FakeNewsDetectorApi(APIView):

	def post(self, request):
		"""
		Decides if data provided in request body parameters contain fake news
		or not. If both `post_text` and `news_text` are provided, the result 
		will reflect the truth value of evaluating `post_text` or `news_text`.
		Neither parameter is required, and either can be provided.

		#TODO: curl example?

		@param request - a rest_framework.request.Request object with any of the 
						following body parameters:
				- post_text: string, contains the plain text body of the Facebook
							post to evaluate 
				- news_text: string, contains the plain text of the news title
							banner attached to the Facebook post to evaluate 

		@return result - a rest_framework.response.Response object containing 
						the results of the evaluation of the body parameter data:
				- fake: boolean, whether overall post was determined to
							contain fake news.
				- confidence: float, the certainty of the post being fake.
							(Range 0-1, 0.0 being certainty of post being real,
							1.0 being certainty of post being fake.)
		"""
		post_text = request.data['post_text'] if 'post_text' in request.data else None
		news_text = request.data['news_text'] if 'news_text' in request.data else None

		evaluation, confidence = determinator.evaluate_post(post_text, news_text) 

		result = {'fake': evaluation, 'confidence': confidence} 
		return Response(data=result)


	def options(self, request):
		"""
		Method for handling CORS preflight requests. This is a public API, so
		all origins are allowed.
		Returns an HTTP response containing only the below headers.
		"""
		headers = {
			'Access-Control-Allow-Origin': "*",
			'Access-Control-Allow-Methods': ["POST", "OPTIONS"],
			'Access-Control-Allow-Headers': [
			    'accept',
			    'accept-encoding',
			    'authorization',
			    'content-type',
			    'dnt',
			    'origin',
			    'user-agent',
			    'x-csrftoken',
			    'x-requested-with',
			],
			'Content-Type': "application/json",
		}
		return Response(data={}, headers=headers)

