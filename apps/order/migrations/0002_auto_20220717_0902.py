# Generated by Django 3.2.7 on 2022-07-17 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at'], 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('cash', 'Card'), ('Credit card', 'Debit card')], max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('received', 'New'), ('in-process', 'In process'), ('delivered', 'Delivered'), ('deleted', 'Deleted'), ('cancelled', 'Cancelled')], default='received', max_length=15),
        ),
    ]
