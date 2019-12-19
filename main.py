import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from data.models import Feedback


def get_feedbacks() -> tuple:
    """Get feedbacks texts and marks"""
    feedbacks_ = [mark[0] for mark in Feedback.objects.values_list('text')]
    marks_ = [mark[0] for mark in Feedback.objects.values_list('mark')]
    return feedbacks_, marks_


feedbacks, marks = get_feedbacks()
