# Generated by Django 2.1.7 on 2019-03-08 03:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispatch_id', models.CharField(default='', max_length=100)),
                ('assistanceType', models.CharField(choices=[('Emergency Ambulance', 'Emergency Ambulance'), ('Rescue and Evacuation', 'Rescue and Evacuation'), ('Fire-Fighting', 'Fire-Fighting'), ('Gas Leak Control', 'Gas Leak Control')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GovernmentAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phoneNumber', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_type', models.CharField(choices=[('Dengue Outbreak', 'Dengue Outbreak'), ('Terrorist', 'Terrorist'), ('Haze', 'Haze')], max_length=100)),
                ('area', models.CharField(max_length=100)),
                ('region', models.CharField(choices=[('Central Region', 'Central Region'), ('East Region', 'East Region'), ('North Region', 'North Region'), ('North-East Region', 'North-East Region'), ('West Region', 'West Region')], max_length=100)),
                ('status', models.CharField(choices=[('Reported', 'Reported'), ('Handling', 'Handling'), ('Closed', 'Closed')], default='Reported', max_length=100)),
                ('level', models.CharField(choices=[('CAT1', 'CAT1'), ('CAT2', 'CAT2')], max_length=100)),
                ('address', models.TextField()),
                ('postal_code', models.IntegerField()),
                ('num_casualties', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('managedBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PublicSubcriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.IntegerField(unique=True)),
                ('region', models.CharField(choices=[('Central Region', 'Central Region'), ('East Region', 'East Region'), ('North Region', 'North Region'), ('North-East Region', 'North-East Region'), ('West Region', 'West Region')], max_length=100)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporterFirstName', models.CharField(default='', max_length=100)),
                ('reporterLastName', models.CharField(default='', max_length=100)),
                ('phoneNumber', models.IntegerField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseapp.Incident')),
            ],
        ),
        migrations.AddField(
            model_name='assistance',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseapp.Report'),
        ),
    ]
