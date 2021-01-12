from django.db import models
class Like(models.Model):
    l_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=30)
    b_id = models.IntegerField()
    state = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'like'
        unique_together = (('user_id','b_id'),)
