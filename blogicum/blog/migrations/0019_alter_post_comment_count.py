# Generated by Django 4.2.3 on 2023-07-22 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_post_comment_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
    ]
