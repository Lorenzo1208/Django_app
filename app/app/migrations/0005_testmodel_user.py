# Generated by Django 4.2.5 on 2023-09-20 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_testmodel_remove_stresslevelform_patient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='testmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]