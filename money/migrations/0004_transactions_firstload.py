# Generated by Django 2.2.5 on 2019-10-01 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0003_auto_20190827_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='firstLoad',
            field=models.BooleanField(default=False),
        ),
    ]
