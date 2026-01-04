from django.http import HttpResponse

# Create your views here.

def home(_request):
    return HttpResponse("Hello from Products Home")
