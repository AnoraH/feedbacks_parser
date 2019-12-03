from django.db import models


class Feedback(models.Model):
    """Feedback model"""

    MARK_GOOD_CHOICE = 1
    MARK_NEUTRAL_CHOICE = 0
    MARK_BAD_CHOICE = -1

    MARK_CHOICES = (
        (MARK_GOOD_CHOICE, 'good'),
        (MARK_NEUTRAL_CHOICE, 'neutral'),
        (MARK_BAD_CHOICE, 'bad')
    )

    preview = models.CharField(max_length=60, null=True, unique=True)
    text = models.TextField()
    mark = models.CharField(max_length=2, choices=MARK_CHOICES)
