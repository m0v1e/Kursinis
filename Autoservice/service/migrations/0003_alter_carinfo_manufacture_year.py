# Generated by Django 4.2.4 on 2023-10-05 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_rename_year_carinfo_manufacture_year_carinfo_engine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carinfo',
            name='manufacture_year',
            field=models.DateField(),
        ),
    ]
