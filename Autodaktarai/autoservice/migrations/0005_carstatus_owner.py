# Generated by Django 4.2.4 on 2023-10-11 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autoservice', '0004_alter_carinfo_car_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='carstatus',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]