from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from submit import helpers
from submit.forms import TaskSubmitForm
from submit.models import Submit
from tasks.models import TaskSet, Task, Stalker, Active


@login_required
def task_set_view(request, pk):  # zobrazenie sady ako zoznam
    task_set = get_object_or_404(TaskSet, pk=pk)

    if not TaskSet.can_see(task_set, request.user):
        raise Http404

    # vytvori sa alebo updatne aktualna sada
    act = Active.objects.get_or_create(user=request.user)
    a = act[0]
    a.task_set = task_set
    a.save()

    # zoznam uloh v sade; iba tie, ktorym moze vidiet zadania v zozname
    q = Task.objects.filter(task_set=task_set)
    q_ids = [o.id for o in q if Task.can_see(o, request.user, 't')]
    tasks = q.filter(id__in=q_ids)

    # zoznam sad do horneho menu; iba tie, ktore user moze vidiet
    q = TaskSet.objects.order_by('title')
    q_ids = [o.id for o in q if TaskSet.can_see(o, request.user)]
    sets = q.filter(id__in=q_ids)

    # roztriedenie uloh na kategorie (ci su vyriesene/precitane)
    # v tomto poradi sa mu aj zobrazuju
    task_cat = []
    task_cat.append({'tasks': [], 'type': 'act_sub'})  # 0
    task_cat.append({'tasks': [], 'type': 'act_read'})  # 1
    task_cat.append({'tasks': [], 'type': 'sol_sub'})  # 2
    task_cat.append({'tasks': [], 'type': 'sol_read'})  # 3
    for task in tasks:
        if Task.is_solved(task, request.user):
            if task.type == Task.SUBMIT:
                task_cat[2]['tasks'].append(task)
            elif task.type == Task.READ:
                task_cat[3]['tasks'].append(task)
        elif Task.is_enabled(task, request.user):
            if task.type == Task.SUBMIT:
                task_cat[0]['tasks'].append(task)
            elif task.type == Task.READ:
                task_cat[1]['tasks'].append(task)

    return render_to_response('tasks/task_set.html',
                              {
                                  'active_app': 'tasks',  # kvoli havnemu menu
                                  'task_set': task_set,  # aktualna sada
                                  'sets': sets,  # viditelne sady v taboch
                                  'style': 'list',  # styl zobrazovania sady
                                  'categories': task_cat,  # ulohy podla kategorii
                                  'tasks': tasks,  # danej sady
                              },
                              context_instance=RequestContext(request))


@login_required
def task_set_graph_view(request, pk=False):  # zobrazenie sady ako graf

    # ak sme nespecifikovali sadu (menu->Ulohy), zobrazi sa/vytvori sa aktivna
    if not pk:
        act = Active.objects.get_or_create(user=request.user)
        pk = act[0].task_set.id

    task_set = get_object_or_404(TaskSet, pk=pk)

    if not TaskSet.can_see(task_set, request.user):
        raise Http404

    # vytvori sa alebo updatne aktualna sada
    act = Active.objects.get_or_create(user=request.user)

    a = act[0]
    a.task_set = task_set
    a.save()

    # zoznam uloh v sade; iba tie, o ktorych moze vediet

    q = Task.objects.filter(task_set=task_set)
    q_ids = [o.id for o in q if Task.can_see(o, request.user, 'g')]
    tasks = q.filter(id__in=q_ids)

    # zoznam sad do horneho menu; iba tie, ktore user moze vidiet
    q = TaskSet.objects.order_by('title')
    q_ids = [o.id for o in q if TaskSet.can_see(o, request.user)]
    sets = q.filter(id__in=q_ids)

    # roztriedime kvoli vykreslovaniu v grafe
    solved_tasks = []
    actual_tasks = []
    invis_tasks = []
    for task in tasks:
        if Task.is_solved(task, request.user):
            solved_tasks.append(task)
        elif Task.is_enabled(task, request.user):
            actual_tasks.append(task)
        else:
            invis_tasks.append(task)

    return render_to_response('tasks/task_set_graph.html',
                              {
                                  'active_app': 'tasks',  # hlavne menu
                                  'task_set': task_set,  # aktualna sada
                                  'sets': sets,  # vsetky sady
                                  'style': 'graph',  # styl zobrazovania sady
                              },
                              context_instance=RequestContext(request))


@login_required
def task_view(request, pk):  # zadanie ulohy
    task = get_object_or_404(Task, pk=pk)

    if not Task.can_see(task, request.user, 't'):
        raise Http404

    # vytvorime alebo updatneme aktivnu ulohu
    act = Active.objects.get_or_create(user=request.user)
    if task.type == task.SUBMIT:
        a = act[0]
        a.task = task
        a.save()

    # ak sa submitovalo
    error = False
    if request.method == 'POST':
        form = TaskSubmitForm(request.POST, request.FILES)
        if form.is_valid():
            submit_id = helpers.process_submit(
                request.FILES['submit_file'],
                task,
                form.cleaned_data['language'],
                request.user)
            if submit_id[0]:
                return HttpResponseRedirect(reverse('submit:protocol', args=(submit_id[1],)) + '#protocol')
            else:
                error = submit_id[1]
        else:
            error = 'file-error'

    # pridame seen
    stalker = Stalker(user=request.user, task=task, seen=datetime.now())
    stalker.save()

    form = TaskSubmitForm()
    submits = Submit.objects.filter(task=pk, user=request.user).order_by('-timestamp')
    is_solved = Task.is_solved(task, request.user)

    return render_to_response('tasks/task.html',
                              {
                                  'active_app': 'tasks',  # hlavne menu
                                  'active': 'text',  # ci si pozerame zadanie alebo vzorak
                                  'is_solved': is_solved,  # kvoli linku v taboch
                                  'task': task,
                                  'form': form,  # submitovaci formular
                                  'submits': submits,  # doterajsie submity v ulohe
                                  'error': error,  # chyba suboru / nepodarene pripojenie na testovac
                                  # momentalne lognuty (kvoli odkazu na riesenie pre adminov)
                                  'req_user': request.user,
                              },
                              context_instance=RequestContext(request))


@login_required
def example_solution_view(request, pk):  # vzorak
    task = get_object_or_404(Task, pk=pk)

    if not Task.can_see(task, request.user, 's'):
        raise Http404

    if task.type == task.READ:
        raise Http404

    return render_to_response('tasks/example_solution.html',
                              {
                                  'is_solved': Task.is_solved(task, request.user),  # kvoli linku v taboch
                                  'active_app': 'tasks',  # hlavne menu
                                  'active': 'ex_sol',  # ci sa zobrazuje zadanie alebo vzorak
                                  'task': task,
                              },
                              context_instance=RequestContext(request))
