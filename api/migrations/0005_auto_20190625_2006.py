# Generated by Django 2.2 on 2019-06-25 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190625_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender_name',
            field=models.CharField(default='undefined', max_length=100),
        ),
    ]
