from django.db import models, migrations


def group_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    permissions = apps.get_model("auth", "Permission")
    group_admin = Group.objects.filter(name__in=["Admin", "WeedMatch"])
    for group in group_admin:
        if group.name == 'Admin':
            permission_admin = permissions.objects.all()
            group.permissions.add(*permission_admin)
        else:
            permissions_weematch = permissions.objects.filter(name__in = ['Can add image','Can change image','Can delete image',
                                                                'Can add image profile','Can delete image profile',
                                                                'Can add credit card', 'Can change credit card', 
                                                                'Can delete credit card'])
            group.permissions.add(*permissions_weematch)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0099_add_group'),
    ]

    operations = [
        migrations.RunPython(group_migration)
    ]