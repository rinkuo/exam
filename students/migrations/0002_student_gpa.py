# Generated by Django 5.1.6 on 2025-02-13 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='gpa',
            field=models.CharField(choices=[('1', '1'), ('1.5', '1.5'), ('2', '2'), ('2.5', '2.5'), ('3', '3'), ('3.5', '3.5'), ('4', '4.5'), ('4.5', '4.5'), ('5', '5')], default='0', max_length=10),
        ),
    ]
