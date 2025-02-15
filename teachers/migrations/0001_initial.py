# Generated by Django 5.1.6 on 2025-02-12 17:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('departments', '0001_initial'),
        ('subjects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('qualification', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=13)),
                ('address', models.TextField()),
                ('join_date', models.DateField()),
                ('position', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='teachers/')),
                ('employment_type', models.CharField(choices=[('full', 'Full Time'), ('part', 'Part Time'), ('contract', 'Contract')], max_length=8)),
                ('status', models.CharField(choices=[('ac', 'Active'), ('in', 'Inactive'), ('pd', 'Pending')], default='in', max_length=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='departments.department')),
                ('subjects', models.ManyToManyField(related_name='teachers', to='subjects.subject')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
