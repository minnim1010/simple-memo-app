from django.db import models
from django.contrib.auth.models import User

class Memo(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField()

    def __str__(self):
        return self.title