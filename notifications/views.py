from django.shortcuts import render
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from weedmatch.settings import EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
import string
import random
from weedmatch import settings


def code_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def welcome(user, request):
    try:
        to = user.email
        data = {'msg': 'Welcome to WeedMatch',
                'username': user.username,
                'url': settings.URL,
                }
        subject, from_email = data['msg'], EMAIL_HOST_USER
        text_content = render_to_string("email/welcome.html", data)
        html_content = render_to_string("email/welcome.html", data)
        send = EmailMultiAlternatives(subject, text_content, from_email, [to],
                                      headers={'From': 'WeedMatch <' + from_email + '>',
                                               'Reply-to': 'WeedMatch <' + from_email + '>'})
        send.attach_alternative(html_content, "text/html")
        send.send()
        return True
    except:
        return False

def recover_password(user, request):
    try:
        new_code = code_generator(20)
        to = user.email
        data = {'msg': 'Your new password',
                'code': new_code,
                'username': user.username,
                'url': settings.URL,
                }
        subject, from_email = data['msg'], EMAIL_HOST_USER
        text_content = render_to_string("email/recover_password.html", data)
        html_content = render_to_string("email/recover_password.html", data)
        send = EmailMultiAlternatives(subject, text_content, from_email, [to],
                                      headers={'From': 'WeedMatch <'+from_email+'>',
                                      'Reply-to': 'WeedMatch <'+from_email+'>'})
        send.attach_alternative(html_content, "text/html")
        send.send()
        user.recovery = new_code
        user.save()
        return True
    except:
        return False