# Generated by Django 2.0.2 on 2018-03-05 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='cod_security',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Code_Security'),
        ),
    ]
