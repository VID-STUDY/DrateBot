# Generated by Django 2.2.3 on 2019-08-17 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('revoratebot', '0006_sossignal_department_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dispatcher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revoratebot.User'),
        ),
    ]