from rest_framework.response import Response
from rest_framework.views import APIView

from common.ocr.imageocr import ImageOCR
from common.ai.determinators import FakeDeterminator


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
		image_url = request.data['image_url'] if 'image_url' in request.data else None
		image_text = None

		# perform OCR on image, if there is one  (This can take upwards of 30 seconds!)
		#(TODO: more efficient way to do this? avoid rebuilding object every time? test latency w/ and w/o OCR. Option to turn off OCR?)
		#if image_url:
		#	ocr = ImageOCR()
		#	text_lines = ocr.recognize(image_url)
		#	image_text = ' '.join(text_lines)
		determinator = FakeDeterminator()
		#TODO: debug
		#print(post_text)
		#print(image_text)
		evaluation = determinator.evaluate_post(post_text)

		result = {'fake': evaluation, 'determinator': 'newsApi', 'probability': 1.00} 
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

