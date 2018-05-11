from django.http import HttpResponse

def index_view(request):
	return HttpResponse("This is my home page.", content_type="text/plain")
