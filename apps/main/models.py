from __future__ import unicode_literals
from django.db import models
from ..login.models import User, UserManager
import datetime
class TaskManager(models.Manager):

    def todays_tasks(self, user_id):
        return self.filter(creator=user_id, date=datetime.date.today())
    def future_tasks(self, user_id):
        return self.filter(creator=user_id, date__gt=datetime.date.today()).order_by('title').distinct


def validate_future_date(value):
    if value < datetime.date.today():
        raise ValidationError(_('Today\'s date or some date in the future please!'))


class Task(models.Model):
    title = models.CharField(max_length=255)
    STATUS_CHOICES = (
        (1, 'Done'),
        (2, 'Pending'),
        (3, 'Missed'),
    )
    status = models.IntegerField(default = 2, choices=STATUS_CHOICES)
    date = models.DateField(auto_now_add=False, auto_now=False, validators=[validate_future_date])
    time = models.TimeField(auto_now=False, auto_now_add=False)
    creator =  models.ForeignKey(User, related_name="itemcreator", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    taskMgr = TaskManager()
    objects = models.Manager()

    def is_done(self):
        return self.status == 1
