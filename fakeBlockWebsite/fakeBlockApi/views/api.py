from django.http import JsonResponse
#from rest_framework.reverse import reverse
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.views import View


# URL /api/fake
class FakeNewsDetectorApi(APIView):

	def get(self, request):
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
							final judgement for `isfake`
							possible values=['factApi', 'neuralNet']
				- probability: float, the certainty of the neural net's 
							prediction if `determinator` is 'neuralNet'
							(is always 1.0 when `determinator` is 'factApi')
		"""
		post_text = request.data['post_text'] if 'post_text' in request.data else None
		image_url = request.data['image_url'] if 'image_url' in request.data else None

		#TODO evaluate


		result = {'fake': False, 'determinator': 'newsApi', 'probability': 1.00} 
		return JsonResponse(result)