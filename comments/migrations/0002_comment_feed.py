# Generated by Django 3.2.6 on 2021-08-23 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='feed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='feeds.feed', verbose_name='피드'),
        ),
    ]
