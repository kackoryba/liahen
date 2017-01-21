# -*- coding: utf8 -*-
from django.db import models
from django.conf import settings

class Submit(models.Model):
    OK = 'OK'
    QUEUE = 'In queue...'

    STATS = {
        'OK': OK,
        'QUEUE': QUEUE,
        'WA': 'Wrong answer',
        'TO': 'Time limit exceeded',
        'IN': 'Internal error',
        'CE': 'Compilation error',
        'RE': 'Runtime exception',
        'SE': 'Security exception',
        }

    LANGUAGE_CHOICES = (
         (".", u"""Zisti podľa prípony"""),
         (".cc", "C++ (.cpp/.cc)"),
         (".pas", "Pascal (.pas/.dpr)"),
         (".c", "C (.c)"),
         (".py", "Python 2.5 (.py)"),
         (".py3", "Python 3.1 (.py3)"),
         (".hs", "Haskell (.hs)"),
         (".cs", "C# (.cs)"),
         (".java", "Java (.java)")
        )

    EXTMAPPING = {
        ".cpp": ".cc",
        ".cc":  ".cc",
        ".pp":  ".pas",
        ".pas": ".pas",
        ".dpr": ".pas",
        ".c":   ".c",
        ".py":  ".py",
        ".py3": ".py3",
        ".hs":  ".hs",
        ".cs":  ".cs",
        ".java":".java"
        }
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL)  #clovek
    task = models.ForeignKey('tasks.Task')  #uloha
    timestamp = models.DateTimeField(   #cas submitu
        auto_now_add=True
        )
    message = models.CharField( #pekna sprava z testovaca (nie skratka)
        max_length = 256, 
        default=QUEUE
        )
    scores = models.FloatField( #ak je uloha na body
        blank=True, 
        null=True
        )
    runtime = models.IntegerField(  #cas behu
        blank=True, 
        default=-1, 
        null=True
        )
    memory = models.IntegerField(   #spotreba pamate
        blank=True, 
        default=-1, 
        null=True
        )
    language = models.CharField(    #progr. jazyk
        max_length = 20,
        choices = LANGUAGE_CHOICES        
        )
    log = models.TextField (    #detailny na vstupy
        default=""
        )

    def __unicode__(self):
        return u'%s | %s | %s | %s' % (self.user, self.task, self.timestamp.strftime('%d-%m-%Y %H:%M:%S'), self.message)
