from django.shortcuts import render


def index(request):
    context_dict = {
        "test": "ecopoints"
    }
    return render(request, 'ecopoints/index.html', context=context_dict)

def about(request):
    return render(request, 'ecopoints/about.html')

def insights(request):
    return render(request, 'ecopoints/insights.html')