from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from rest_framework.status import HTTP_400_BAD_REQUEST
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

# URL about/
class AboutPage(View):
	def get(self, request):
		"""
		Return the HTML template for the about page.

		@param request - a rest_framework.request.Request object. There are
						no body parameters.
		@return - a TemplateResponse object that loads the about HTML template
		"""
		return TemplateResponse(request, 'about.html', {})

# URL api/
class ApiDocsPage(View):
	def get(self, request):
		"""
		Return the HTML template for the api docs page.

		@param request - a rest_framework.request.Request object. There are
						no body parameters.
		@return - a TemplateResponse object that loads the api HTML template
		"""
		return TemplateResponse(request, 'api.html', {})