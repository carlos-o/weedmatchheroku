from __future__ import absolute_import, unicode_literals
from celery import shared_task
from accounts import models as accounts_models


@shared_task
def disableCodeRecoveryPassword(instance):
    instance = accounts_models.User.objects.get(id=instance)
    instance.recovery = ''
    instance.save()
    return True