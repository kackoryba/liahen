# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Active',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stalker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seen', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.SlugField(help_text='Nesmie by\u0165 zhodn\xe9 s inou \xfalohou na Experimente.', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('text', models.TextField(default='Rozpravka\n####\xdaloha\n\n####Form\xe1t vstupu\n\n####Form\xe1t v\xfdstupu\n\n####Pr\xedklad\n\n<table class = "table io-table">\n  <tr>\n    <th>Vstup</th>\n    <th>V\xfdstup</th>\n  </tr>\n  <tr>\n    <td><pre></pre></td>\n    <td><pre></pre></td>\n  </tr>\n</table>', help_text=b'Obsah bude prehnan\xc3\xbd <a href="http://en.wikipedia.org/wiki/Markdown">Markdownom</a>.')),
                ('example_solution', models.TextField(default='\n<pre class = "prettyprint">Escape-nuty zdrojak</pre>\n', help_text=b'Obsah bude prehnan\xc3\xbd <a href="http://en.wikipedia.org/wiki/Markdown">Markdownom</a>. <br />Zdroj\xc3\xa1k mus\xc3\xad by\xc5\xa5 <a href="http://www.htmlescape.net/htmlescape_tool.html">escape-nut\xc3\xbd od special chars</a>.<br /> Pou\xc5\xbe\xc3\xadvajte na\xc5\x88 tag <code>&lt;pre&gt;&lt;/pre&gt;</code> (blokov\xc3\xbd) alebo <code>&lt;code&gt;&lt;/code&gt;</code> (riadkov\xc3\xbd). Na syntax highlight pridajte <code>&lt;pre class = &quot;prettyprint&quot;&gt;&lt;/pre&gt;</code>.', blank=True)),
                ('public', models.BooleanField(default=True)),
                ('type', models.CharField(default=b'S', max_length=1, choices=[(b'S', b'Submit'), (b'R', b'Read')])),
                ('prereqs', models.ManyToManyField(related_name='prevs', to='tasks.Task', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskSet',
            fields=[
                ('id', models.SlugField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('public', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='task_set',
            field=models.ForeignKey(to='tasks.TaskSet'),
        ),
        migrations.AddField(
            model_name='task',
            name='timestamps',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='tasks.Stalker'),
        ),
        migrations.AddField(
            model_name='stalker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='stalker',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='active',
            name='task',
            field=models.ForeignKey(default=b'submit', to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='active',
            name='task_set',
            field=models.ForeignKey(default=b'intro', to='tasks.TaskSet'),
        ),
        migrations.AddField(
            model_name='active',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
