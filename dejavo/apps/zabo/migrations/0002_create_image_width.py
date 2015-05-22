# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def save_image_once(apps, schema_editor):
    model = apps.get_model('zabo', 'article')
    for article in model.objects.all():
        article.save()


class Migration(migrations.Migration):

    dependencies = [
        ('zabo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image_width',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(width_field=b'image_width', upload_to=b'poster'),
            preserve_default=True,
        ),
        migrations.RunPython(save_image_once),   # To create height and width, save each image once
    ]
