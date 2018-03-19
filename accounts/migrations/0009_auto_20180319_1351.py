# Generated by Django 2.0.2 on 2018-03-19 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20180316_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='match_sex',
            field=models.CharField(blank=True, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Otro', 'Otro')], default='Otro', max_length=10, null=True, verbose_name='Match_sex'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Otro', 'Otro')], default='Otro', max_length=10, null=True, verbose_name='Type_sex'),
        ),
    ]
