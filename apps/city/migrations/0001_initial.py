# Generated by Django 3.2.7 on 2022-07-17 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255, verbose_name='City')),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
    ]