# Generated by Django 4.2.3 on 2023-07-22 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_comment_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='count',
        ),
    ]
