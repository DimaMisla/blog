# Generated by Django 4.2.2 on 2023-07-02 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_category_options_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='author',
        ),
    ]
