from django.http import JsonResponse
#from rest_framework.reverse import reverse
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.views import View
#from .decorators import define_usage
from rest_framework.decorators import api_view


class ApiIndex(View):
	@api_view(['GET'])
	def get(self, request):
		return JsonResponse({})