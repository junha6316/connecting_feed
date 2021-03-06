# Generated by Django 3.2.6 on 2021-08-23 01:16

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('body', models.TextField(verbose_name='내용')),
                ('random_nickname', models.CharField(default=core.models.default_random_name, max_length=20)),
                ('image', models.ImageField(null=True, upload_to=core.models.image_directory)),
                ('audio', models.FileField(blank=True, null=True, upload_to=core.models.audio_directory)),
                ('gif', models.FileField(blank=True, null=True, upload_to=core.models.gif_directory)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='comments.comment', verbose_name='코멘트')),
            ],
            options={
                'db_table': 'comments',
                'ordering': ['created_at'],
            },
        ),
    ]
