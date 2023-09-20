# Generated by Django 4.2.5 on 2023-09-20 11:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_testmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='stressevaluationform',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stressevaluationform',
            name='score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]