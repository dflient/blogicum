# Generated by Django 4.2.3 on 2023-07-22 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_post_comment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='count',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]