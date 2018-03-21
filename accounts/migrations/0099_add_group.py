from django.db import models, migrations


def group_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=u'Admin'),
        Group(name=u'WeedMatch'),
        Group(name=u'WeedMatchVip'),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20180320_1954'),
    ]

    operations = [
        migrations.RunPython(group_migration)
    ]