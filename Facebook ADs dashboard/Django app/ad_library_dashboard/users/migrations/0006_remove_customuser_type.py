# Generated by Django 4.0.5 on 2022-10-03 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='type',
        ),
    ]