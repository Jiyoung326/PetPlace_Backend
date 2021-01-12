from django.db import models

# Create your models here.
class BookMark(models.Model):
    m_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=30)
    f_id = models.CharField(max_length=10)
    state = models.CharField(max_length=10,default='정상')

    class Meta:
        managed = False
        db_table = 'bookmark'