from django.template.response import TemplateResponse
from django.http import HttpResponse
#from django.http import JsonResponse
#from rest_framework.reverse import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.views import View
from rest_framework.decorators import api_view


# URL /
@api_view(['GET'])
def demo_index_page(request):
	print(type(request))
	return TemplateResponse(request, 'home.html', {})