from django.shortcuts import render


# Create your views here.
def intro_view(request):
    return render(request, 'about/intro.html')
