from django.shortcuts import render

# Create your views here.

def index(request):
    context_dict = {
        "test": "Hello World!"
    }
    return render(request, 'ecopoints/index.html', context=context_dict)

def insights(request):
    return render(request, 'ecopoints/insights.html')