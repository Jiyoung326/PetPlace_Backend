from django.db import models

class PhotoBoard(models.Model):
    b_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.CharField(max_length=300)
    regdate = models.DateField()
    update_date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=10)

    class Meta:
        managed = False
        ordering = ['-b_id']
        db_table = 'photo_board'