from rest_framework.response import Response
from rest_framework.views import APIView
from common.ocr.imageocr import ImageOCR

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

		# perform OCR on image, if there is one (TODO: more efficient way to do this? avoid rebuilding object every time?)
		if image_url:
			ocr = ImageOCR()
			text_lines = ocr.recognize(image_url)
			image_text = ' '.join(text_lines)

		#TODO: debug
		print(post_text)
		print(image_text)

		result = {'fake': False, 'determinator': 'newsApi', 'probability': 1.00} 
		return Response(result)

