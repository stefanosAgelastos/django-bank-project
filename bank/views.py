from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'bank/index.html', context)
