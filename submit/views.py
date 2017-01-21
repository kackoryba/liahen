from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from tasks.models import Task, Active
from submit.models import Submit


@login_required
# rozne filtre na tabulku submitov; podla 'type'
def judge_view(request, type, task='', user=''):
    # defaultne hodnoty pre parametre do returnu
    cur_task = ''
    cur_user = ''
    tasks = ''

    if type == 'me':  # moje
        submits = Submit.objects.filter(
            user=request.user).order_by('-timestamp')

    elif type == 'now':  # aktualne
        submits = Submit.objects.order_by('-timestamp')[:10]

    elif type == 'task':  # vsetky uspesne v ulohe
        submits = Submit.objects.filter(
            task=task, message=Submit.OK).order_by('-timestamp')
        cur_task = get_object_or_404(Task, pk=task)
        if request.user.is_staff and request.user.is_active:
            tasks = Task.objects.filter(type=Task.SUBMIT)
        else:
            q = Task.objects.filter(public=True, type=Task.SUBMIT)
            q_ids = [o.id for o in q if o.task_set.public]
            tasks = q.filter(id__in=q_ids)

    # iba pre adminov:
    elif (request.user.is_staff and request.user.is_active):
        if type == 'user':  # vsetky userove
            cur_user = get_object_or_404(User, username=user)
            submits = Submit.objects.filter(
                user=cur_user).order_by('-timestamp')

        elif type == 'user_task':  # vsetky userove v ulohe
            cur_user = get_object_or_404(User, username=user)
            submits = Submit.objects.filter(
                user=cur_user, task=task).order_by('-timestamp')
            cur_task = get_object_or_404(Task, pk=task)
            tasks = Task.objects.all()

    else:
        raise Http404

    # aktivna uloha sa defaultne zobrazi vo filtri podla ulohy
    act = Active.objects.get_or_create(user=request.user)
    active_task = act[0].task.id
    
    return render(request, 'submit/judge.html',
                             {
                             'active_app':'submit', #kvoli menu hore
                             'submits':submits, #tabulka submitov
                             'type':type,   #typ filtra
                             'tasks':tasks, #viditelne ulohy pre search-box podla ulohy
                             'cur_task':cur_task,   #filtre podla ulohy
                             'cur_user':cur_user,   #filtre podla cloveka
                             'req_user':request.user,   #prihlaseny user
                             'active_task':active_task,   #aktivna uloha
                             }, 
                             )
                              

@login_required
def protocol_view(request, pk):  # protokol z testovania
    submit = get_object_or_404(Submit, pk=pk)

    # ak si ho chce pozriet cudzi user, ktory nie je admin
    if not ((request.user.is_active and request.user.is_staff) or submit.user == request.user):
        raise Http404

    source_path = settings.PROJECT_PATH + '/../submit/submits/' + \
        str(submit.user.username) + '/' + str(submit.task.id) + '/' + str(submit.id) + '.data'

    source_code = open(source_path, 'r').read()

    return render(request, 'submit/protocol.html',
                              {
                               #'active_app':'submit',
                               'submit':submit,
                               'source_code':source_code,
                               },
                              )



@csrf_exempt
def update_submit(request):  # spracovanie submitu po odpovedi testovaca
    if (request.method == 'POST'):
        # data z testovaca k sebe do db
        id = request.POST['submit_id']

        submit = get_object_or_404(Submit, pk=id)

        message = request.POST['result']
        # slovny popis (WA -> Wrong answer)
        if message in Submit.STATS:
            submit.message = Submit.STATS[message]
        else:
            submit.message = message

        submit.runtime = request.POST['time']
        submit.memory = request.POST['memory']
        submit.log = request.POST['log']

        submit.save()
    return HttpResponse("Ty si chudak")
