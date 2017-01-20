# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(default=b'In queue...', max_length=256)),
                ('scores', models.FloatField(null=True, blank=True)),
                ('runtime', models.IntegerField(default=-1, null=True, blank=True)),
                ('memory', models.IntegerField(default=-1, null=True, blank=True)),
                ('language', models.CharField(max_length=20, choices=[(b'.', 'Zisti pod\u013ea pr\xedpony'), (b'.cc', b'C++ (.cpp/.cc)'), (b'.pas', b'Pascal (.pas/.dpr)'), (b'.c', b'C (.c)'), (b'.py', b'Python 2.5 (.py)'), (b'.py3', b'Python 3.1 (.py3)'), (b'.hs', b'Haskell (.hs)'), (b'.cs', b'C# (.cs)'), (b'.java', b'Java (.java)')])),
                ('log', models.TextField(default=b'')),
                ('task', models.ForeignKey(to='tasks.Task')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
