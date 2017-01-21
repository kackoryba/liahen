from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from tasks.models import TaskSet, Task, Stalker, Active
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from submit.forms import TaskSubmitForm
from submit.models import Submit
from django import forms
from submit import helpers
import pygraphviz as pgv
from datetime import datetime, date, time

from django.utils import timezone
    
@login_required
def task_set_view(request, pk): #zobrazenie sady ako zoznam
    task_set = get_object_or_404(TaskSet, pk=pk)
    
    if not TaskSet.can_see(task_set, request.user):
        raise Http404
    
    #vytvori sa alebo updatne aktualna sada
    act = Active.objects.get_or_create(user = request.user)
    a = act[0]
    a.task_set = task_set
    a.save()

    #zoznam uloh v sade; iba tie, ktorym moze vidiet zadania v zozname
    q = Task.objects.filter(task_set=task_set)
    q_ids = [o.id for o in q if Task.can_see(o, request.user, 't')]
    tasks = q.filter(id__in=q_ids)
    
    #zoznam sad do horneho menu; iba tie, ktore user moze vidiet
    q = TaskSet.objects.order_by('title')
    q_ids = [o.id for o in q if TaskSet.can_see(o, request.user)]
    sets = q.filter(id__in=q_ids)
    
    #roztriedenie uloh na kategorie (ci su vyriesene/precitane)
    #v tomto poradi sa mu aj zobrazuju
    task_cat=[]
    task_cat.append({'tasks':[], 'type': 'act_sub'})    #0
    task_cat.append({'tasks':[], 'type': 'act_read'})   #1
    task_cat.append({'tasks':[], 'type': 'sol_sub'})    #2
    task_cat.append({'tasks':[], 'type': 'sol_read'})   #3
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
    
    return render(request, 'tasks/task_set.html',
                              {
                               'active_app':'tasks',    #kvoli havnemu menu
                               'task_set':task_set, #aktualna sada
                               'sets': sets,    #viditelne sady v taboch
                               'style':'list',  #styl zobrazovania sady
                               'categories': task_cat,  #ulohy podla kategorii
                               'tasks':tasks,   #danej sady
                               },
                              )

@login_required
def task_set_graph_view(request, pk=False): #zobrazenie sady ako graf

    #ak sme nespecifikovali sadu (menu->Ulohy), zobrazi sa/vytvori sa aktivna
    if not pk:
        act = Active.objects.get_or_create(user = request.user)
        pk = act[0].task_set.id

    task_set = get_object_or_404(TaskSet, pk=pk)
    
    if not TaskSet.can_see(task_set, request.user):
        raise Http404
    
    #vytvori sa alebo updatne aktualna sada
    act = Active.objects.get_or_create(user = request.user)
    a = act[0]
    a.task_set = task_set
    a.save()
    
    #zoznam uloh v sade; iba tie, o ktorych moze vediet
    q = Task.objects.filter(task_set=task_set)
    q_ids = [o.id for o in q if Task.can_see(o, request.user, 'g')]
    tasks = q.filter(id__in=q_ids)
    
    #zoznam sad do horneho menu; iba tie, ktore user moze vidiet
    q = TaskSet.objects.order_by('title')
    q_ids = [o.id for o in q if TaskSet.can_see(o, request.user)]
    sets = q.filter(id__in=q_ids)
    
    #roztriedime kvoli vykreslovaniu v grafe
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
 
    #nakrmime graf datami
    G=pgv.AGraph(directed=True)
    G.node_attr['color'] = '#dddddd'
    G.node_attr['style'] = 'filled'
    G.node_attr['fontcolor'] = '#ffffff'
    G.node_attr['fontname'] = 'Helvetica, Arial, sans-serif'
    G.graph_attr['bgcolor'] = 'transparent'
    G.edge_attr['color'] = '#555555'
    G.edge_attr['arrowhead'] = 'open'
        
    RED = '#C71C22'
    BLUE_L = '#2FA4E7'
    BLUE_D = '#033C73'
    GREEN = '#73A839'
    ORANGE = '#DD5600'
    
    for task in solved_tasks:
        G.add_node(task.id, 
                   fillcolor = (GREEN if (task.type == Task.SUBMIT) else BLUE_D),
                   shape = ('ellipse' if (task.type == Task.SUBMIT) else 'box'), 
                   tooltip = task.title, 
                   URL = reverse('tasks:task', args=(task.id,)),
                   fontcolor = '#eeeeee'
                   )
    
    for task in actual_tasks:
        G.add_node(task.id,
                   fillcolor = (RED if (task.type == Task.SUBMIT) else BLUE_L), 
                   shape = ('ellipse' if (task.type == Task.SUBMIT) else 'box'), 
                   tooltip = task.title, 
                   URL = reverse('tasks:task', args=(task.id,)),
                   fontcolor = '#ffffff'
                   )
                   
    for task in invis_tasks:
        #admin si vie pozerat aj invis ulohy
        if request.user.is_active and request.user.is_staff:
            G.add_node(task.id,
                    fillcolor = '#ffffff', 
                    shape = ('ellipse' if (task.type == Task.SUBMIT) else 'box'), 
                    tooltip = task.title, 
                    URL = reverse('tasks:task', args=(task.id,)),
                    fontcolor = '#000000'
                    )
        else:
            G.add_node(task.id,
                    label = '', 
                    fillcolor = '#FFFFFF', 
                    shape = ('ellipse' if (task.type == Task.SUBMIT) else 'box'),                    
                    tooltip = ' ', 
                    fontcolor = 'black', 
                    style = 'dashed', 
                    color = '#333333',
                    )

    #najprv trebalo pridat vsetky vrcholy, aby sa im nastavil styl, hrany az potom
    for task in solved_tasks:
        edges = task.prereqs.all()
        for edge in edges:
            G.add_edge(edge.id, task.id, style = 'solid')
    
    for task in actual_tasks:
        edges = task.prereqs.all()
        for edge in edges:
            G.add_edge(edge.id, task.id, style = 'solid')
                   
    for task in invis_tasks:
        edges = task.prereqs.all()
        for edge in edges:
            G.add_edge(edge.id, task.id, style = 'dashed')
                               
    G.layout()

    #vymazeme hlavicky, lebo neincludujeme svg object, ale rovno ho kreslime; inak by sme neboli html valid
    graph = "\n".join(G.draw(format='svg').split('\n')[3:])
    
    return render(request, 'tasks/task_set_graph.html',
                              {
                              'graph':graph, #data pre graf (svg)
                              'active_app':'tasks', #hlavne menu 
                              'task_set':task_set,  #aktualna sada
                              'sets': sets, #vsetky sady
                              'style':'graph',  #styl zobrazovania sady
                              },
                              )

@login_required
def task_view(request, pk): #zadanie ulohy
    task = get_object_or_404(Task, pk=pk)
    
    if not Task.can_see(task, request.user, 't'):
        raise Http404
    
    #vytvorime alebo updatneme aktivnu ulohu
    act = Active.objects.get_or_create(user = request.user)
    if task.type == task.SUBMIT:
        a = act[0]
        a.task = task
        a.save()
    
    #ak sa submitovalo
    error = False
    if request.method == 'POST':
        form = TaskSubmitForm(request.POST, request.FILES)
        if form.is_valid():
            submit_id = helpers.process_submit(request.FILES['submit_file'], task, form.cleaned_data['language'], request.user)
            if submit_id[0]:
                return HttpResponseRedirect(reverse('submit:protocol', args=(submit_id[1],))+'#protocol')
            else:
                error = submit_id[1]
        else:
            error = 'file-error'
    
    #pridame seen
    stalker = Stalker (user = request.user, task = task, seen = timezone.now())
    stalker.save()
    
    form = TaskSubmitForm()
    submits = Submit.objects.filter(task = pk, user = request.user).order_by('-timestamp')
    is_solved = Task.is_solved(task, request.user)

    return render(request, 'tasks/task.html',
                            {
                             'active_app':'tasks',  #hlavne menu
                             'active':'text',   #ci si pozerame zadanie alebo vzorak
                             'is_solved':is_solved, #kvoli linku v taboch
                             'task': task, 
                             'form': form,  #submitovaci formular
                             'submits':submits, #doterajsie submity v ulohe
                             'error':error,    #chyba suboru / nepodarene pripojenie na testovac
                             'req_user': request.user,    #momentalne lognuty (kvoli odkazu na riesenie pre adminov)
                             },
                            )

@login_required
def example_solution_view(request, pk):     #vzorak
    task = get_object_or_404(Task, pk=pk)
    
    if not Task.can_see(task, request.user, 's'):
        raise Http404
    
    if task.type == task.READ:
        raise Http404

    return render(request, 'tasks/example_solution.html',
                              {
                               'is_solved':Task.is_solved(task, request.user),  #kvoli linku v taboch 
                               'active_app':'tasks',    #hlavne menu 
                               'active':'ex_sol',   #ci sa zobrazuje zadanie alebo vzorak
                               'task': task,
                               },
                              )
