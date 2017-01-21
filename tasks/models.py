# -*- coding: utf8 -*-
from django.db import models
import submit.models
from django.contrib.auth.models import User
from markdown import markdown
from django.utils.html import mark_safe

# sada uloh


class TaskSet(models.Model):
    id = models.SlugField(  # kratky nazov
        primary_key=True
    )
    title = models.CharField(  # pekny nazov
        max_length=256
    )
    public = models.BooleanField(  # nie public vidi iba admin
        default=True
    )

    # ak nie je public, moze ju vidiet iba admin
    def can_see(self, user):
        if not self.public:
            if (user.is_active and user.is_staff):
                return True
            return False
        return True

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.id)


# uloha; citaci aj submitovatelny typ
class Task(models.Model):
    TASK_TEMPLATE = u"""Rozpravka
####Úloha

####Formát vstupu

####Formát výstupu

####Príklad

<table class = "table io-table">
  <tr>
    <th>Vstup</th>
    <th>Výstup</th>
  </tr>
  <tr>
    <td><pre></pre></td>
    <td><pre></pre></td>
  </tr>
</table>"""

    EX_SOL_TEMPLATE = u"""
<pre class = "prettyprint">Escape-nuty zdrojak</pre>
"""

    ID_HELP = u"""Nesmie byť zhodné s inou úlohou na Experimente."""

    TEXT_HELP = 'Obsah bude prehnaný <a href="http://en.wikipedia.org/wiki/Markdown">Markdownom</a>.'

    EX_SOL_HELP = 'Obsah bude prehnaný <a href="http://en.wikipedia.org/wiki/Markdown">Markdownom</a>. <br />' \
                  'Zdroják musí byť <a href="http://www.htmlescape.net/htmlescape_tool.html">' \
                  'escape-nutý od special chars</a>.<br /> Používajte naň tag <code>&lt;pre&gt;&lt;/pre&gt;</code> ' \
                  '(blokový) alebo <code>&lt;code&gt;&lt;/code&gt;</code> (riadkový). Na syntax highlight pridajte ' \
                  '<code>&lt;pre class = &quot;prettyprint&quot;&gt;&lt;/pre&gt;</code>.'

    SUBMIT = 'S'
    READ = 'R'
    TYPES = (
        (SUBMIT, 'Submit'),
        (READ, 'Read'),
    )

    id = models.SlugField(  # kratky nazov
        primary_key=True,
        help_text=ID_HELP
    )
    title = models.CharField(  # pekny nazov
        max_length=256
    )
    text = models.TextField(  # zadanie ulohy alebo sprievodny text
        default=TASK_TEMPLATE,
        help_text=TEXT_HELP
    )
    example_solution = models.TextField(  # vzorak submitovatelnych uloch
        blank=True,
        default=EX_SOL_TEMPLATE,
        help_text=EX_SOL_HELP
    )

    public = models.BooleanField(  # nie public vidi iba admin
        default=True
    )

    type = models.CharField(  # ci sa submituje alebo cita
        max_length=1,
        choices=TYPES,
        default=SUBMIT
    )

    task_set = models.ForeignKey(TaskSet)  # do ktorej sady patri

    timestamps = models.ManyToManyField(  # zaznamenava zobrazenie zadania
        User,
        through='Stalker'
    )

    prereqs = models.ManyToManyField(  # preprekvizity (hrany, kt. do mna v grafe vedu)
        "self",
        symmetrical=False,
        related_name='prevs',
        blank=True
    )

    def __unicode__(self):
        return u'%s: %s' % (self.task_set.id, self.id)

    # ak ja som public, ale moja sada nie je
    def _get_is_public(self):
        if self.public and self.task_set.public:
            return True
        return False
    is_public = property(_get_is_public)

    # prezenie cez markdown
    def _get_rendered_text(self):
        return mark_safe(markdown(self.text, safe_mode=False))
    rendered_text = property(_get_rendered_text)

    # prezenie cez markdown
    def _get_rendered_ex_sol(self):
        return mark_safe(markdown(self.example_solution, safe_mode=False))
    rendered_ex_sol = property(_get_rendered_ex_sol)

    # ci je vyriesena userom x
    def is_solved(self, user):
        if self.type == self.SUBMIT:
            n = submit.models.Submit.objects.filter(message=submit.models.Submit.OK, task=self, user=user).count()
            if n > 0:
                return True
            else:
                return False

        elif self.type == self.READ:
            s = Stalker.objects.filter(user=user, task=self)
            if s.count() >= 1:
                return True
            else:
                return False

    # ci user x moze vidiet zadanie = uz ju objavil
    def is_enabled(self, user):
        required = self.prereqs.all()
        for task in required:
            if not Task.is_solved(task, user):
                return False
        return True

    # ci user moze vediet o jej existencii
    def can_see(self, user, field):
        if (user.is_active and user.is_staff):
            return True
        if not self.public:
            return False
        if field == 't':  # text zadania
            if not self.is_enabled(user):
                return False
            return True
        if field == 's':  # solution    #ci je vyriesena userom x

            if not self.is_solved(user):
                return False
            else:
                return True
        if field == 'g':  # invisible ulohy v grafe
            return True
        return False

    # zisti pocet riesitelov (!= pocet OK)
    def _get_num_solvers(self):
        if self.type == self.SUBMIT:
            num = submit.models.Submit.objects.filter(
                message=submit.models.Submit.OK,
                task=self).distinct('user').count()
        elif self.type == self.READ:
            num = -1
        return num
    num_solvers = property(_get_num_solvers)


# loguje zobrazenia zadania; casom sa bude hodit na statistiky a achievementy (napr. ako dlho trva vyriesenie ulohy)
class Stalker(models.Model):
    task = models.ForeignKey(Task)  # ktora uloha
    user = models.ForeignKey(User)  # ktory user
    seen = models.DateTimeField(  # kedy
        null=True
    )

    def __unicode__(self):
        return u'%s | %s | %s' % (self.user, self.task, self.seen)


# ktore ulohy a sady su pre ktoreho uzivatela aktivne (= zobrazuju sa defaultne)
class Active(models.Model):
    user = models.OneToOneField(User)  # ktory user
    task_set = models.ForeignKey(TaskSet, default='intro')  # ktoru sadu
    task = models.ForeignKey(Task, default='submit')  # ktoru ulohu

    # (niekedy v buducnosti) ci ma na pozeranie sady styl graf alebo zoznam
    # GRAPH = 'G'
    # LIST = 'L'
    # task_set_style = models.CharField(max_length = 1, default = GRAPH, choices = ((GRAPH, 'Graph'),(LIST, 'List')))

    def __unicode__(self):
        return u'%s | %s | %s' % (self.user, self.task_set.id, self.task.id)
