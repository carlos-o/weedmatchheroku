# Generated by Django 2.0.2 on 2018-03-05 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='profile', verbose_name='Photo'),
        ),
    ]
