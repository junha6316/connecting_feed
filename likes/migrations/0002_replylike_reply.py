# Generated by Django 3.2.6 on 2021-08-19 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('replies', '0001_initial'),
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='replylike',
            name='reply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_likes', to='replies.reply'),
        ),
    ]
