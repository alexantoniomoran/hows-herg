# Generated by Django 3.0.3 on 2020-04-18 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200418_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagesent',
            name='sent_from_website_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='messagesent',
            name='sent_from_website_text',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]