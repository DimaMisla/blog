# Generated by Django 4.2.2 on 2023-08-06 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_commentlike_commentdislike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]