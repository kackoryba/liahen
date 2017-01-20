from django.shortcuts import render_to_response
from django.template import RequestContext


# Create your views here.
def intro_view(request):
    return render_to_response('about/intro.html', context_instance=RequestContext(request))
