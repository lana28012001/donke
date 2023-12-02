from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')
    def post(self, request):
        pass

def handler404(request,*args, **argv):
    # context = {'exception':exception}
    return render(request, '404.html', status=404)

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)
