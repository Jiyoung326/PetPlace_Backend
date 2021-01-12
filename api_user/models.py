from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=30)
    nickname = models.CharField(max_length=20)
    state = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'user'