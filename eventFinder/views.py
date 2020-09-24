from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse


def index(request):
    context = {}
    if request.user.is_authenticated:
        context['logged_in']=True
    else:
        context['logged_in']=False

    return render(request,'eventFinder/index.html',context)
