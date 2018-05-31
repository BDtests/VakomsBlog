"""
Module responsible for sending emails.
"""

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email(subject, message, recepient_list, template, email_data):
    template = 'emails/' + template
    html_message=render_to_string(template, email_data)
    send_mail(subject,
              message,
              settings.DEFAULT_FROM_EMAIL,
              recepient_list,
              html_message=html_message
              )
