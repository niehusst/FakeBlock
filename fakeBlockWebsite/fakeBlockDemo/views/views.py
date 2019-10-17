from django.template.response import TemplateResponse
from django.http import HttpResponse
#from django.http import JsonResponse
#from rest_framework.reverse import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.views import View
from rest_framework.decorators import api_view


# URL /
class DemoIndex(View):

	def get(self, request):
		"""
		Return the HTML template for the demo page.

		@param request - a rest_framework.request.Request object. There are
						no body parameters.
		@return - a TemplateResponse object that loads the index HTML template
		"""
		return TemplateResponse(request, 'home.html', {})