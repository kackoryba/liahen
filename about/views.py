from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from tasks.models import TaskSet, Task
from django.contrib.auth.decorators import login_required
from submit.forms import TaskSubmitForm
from submit.models import Submit
from tasks.models import Task
import os
from django.conf import settings
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def intro_view(request):    
    return render(request, 'about/intro.html')
