from django.shortcuts import render


# Create your views here.
def intro_view(request):
    return render(request, 'about/intro.html')

def about_view(request):
    return render(request, 'about/about.html')
    
def contact_view(request):
    return render(request, 'about/contact.html')

def terms_view(request):
    return render(request, 'about/terms.html')
