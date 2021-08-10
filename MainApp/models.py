import datetime
from django.db import models
from django.contrib.auth.models import User

LANG_CHOICES = (
    ("py", "python"),
    ("js", "javascript"),
    ("cpp", "C++"),
)

class Snippet(models.Model):
    name = models.CharField(max_length=100, blank=True)
    lang = models.CharField(max_length=30, choices=LANG_CHOICES)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)
