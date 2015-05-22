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
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('subtitle', models.CharField(max_length=150, blank=True)),
                ('location', models.CharField(max_length=200, blank=True)),
                ('content', models.TextField()),
                ('announcement', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to=b'poster')),
                ('category', models.CharField(max_length=20, choices=[(b'recruit', b'\xeb\xa6\xac\xec\xbf\xa0\xeb\xa5\xb4\xed\x8c\x85'), (b'performance', b'\xea\xb3\xb5\xec\x97\xb0'), (b'competition', b'\xeb\x8c\x80\xed\x9a\x8c'), (b'display', b'\xec\xa0\x84\xec\x8b\x9c'), (b'briefing', b'\xec\x84\xa4\xeb\xaa\x85\xed\x9a\x8c'), (b'lecture', b'\xea\xb0\x95\xec\x97\xb0'), (b'event', b'\xed\x96\x89\xec\x82\xac'), (b'etc', b'\xea\xb8\xb0\xed\x83\x80')])),
                ('host_name', models.CharField(max_length=50)),
                ('host_image', models.ImageField(default=b'default/default_host.png', upload_to=b'host')),
                ('host_description', models.CharField(max_length=150)),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('owner', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filepath', models.FileField(upload_to=b'attachment')),
                ('article', models.ForeignKey(related_name='attachment', to='zabo.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_type', models.CharField(max_length=20, choices=[(b'email', b'Email'), (b'phone', b'Phone'), (b'facebook', b'Facebook'), (b'twitter', b'Twitter'), (b'url', b'URL'), (b'etc', b'Etc')])),
                ('info', models.CharField(max_length=200)),
                ('article', models.ForeignKey(related_name='contact', to='zabo.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_private', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(to='zabo.Article')),
                ('writer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timeslot_type', models.CharField(max_length=20, choices=[(b'point', b'Point'), (b'range', b'Range')])),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('is_main', models.BooleanField(default=False)),
                ('label', models.CharField(max_length=50, blank=True)),
                ('article', models.ForeignKey(related_name='timeslot', to='zabo.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='zabo.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='writer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
