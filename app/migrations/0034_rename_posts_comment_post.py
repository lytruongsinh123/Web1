# Generated by Django 5.1 on 2024-09-09 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_rename_post_comment_posts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='posts',
            new_name='post',
        ),
    ]