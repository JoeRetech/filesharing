# Generated by Django 4.2.4 on 2024-03-26 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shared',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=300)),
                ('message', models.CharField(max_length=300)),
                ('recipient_list', models.CharField(max_length=300)),
            ],
        ),
    ]