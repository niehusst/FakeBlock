from rest_framework.response import Response
from rest_framework.views import APIView

from common.ocr.imageocr import ImageOCR
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
		or not. If bost post_text and a image_url are provided, they will be
		evaluated separately.


		@param request - a rest_framework.request.Request object with the 
						following required body parameters:
				- post_text: string, contains the plain text of the Facebook
							post to evaluate (required, but can be None)
				- image_url: string, contains the url of the Facebook
							post image to evaluate (required, but can be None)

		@return result - a JsonResponse object containing the results of the
						evaluation of the body parameter data:
				- fake: boolean, whether overall post was determined to
							contain fake news.
				- determinator: string, what level of the API AI made the
							final judgement for `fake`
							possible values=['factApi', 'neuralNet']
				- probability: float, the certainty of the neural net's 
							prediction if `determinator` is 'neuralNet'
							(is always 1.0 when `determinator` is 'factApi')
		"""
		post_text = request.data['post_text'] if 'post_text' in request.data else None
		news_text = request.data['news_text'] if 'news_text' in request.data else None

		evaluation = determinator.evaluate_post(post_text, news_text) 

		result = {'fake': evaluation, 'determinator': 'newsApi', 'probability': 1.00} #TODO make this reflect results of NN
		return Response(data=result)


	def options(self, request):
		"""
		Method for handling CORS preflight requests. This is a public API, so
		all origins are allowed.
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

