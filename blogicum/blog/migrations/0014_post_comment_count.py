# Generated by Django 4.2.3 on 2023-07-22 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_remove_comment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comment_count',
            field=models.IntegerField(null=True),
        ),
    ]
