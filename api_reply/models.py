# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Reply(models.Model):
    r_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=30)
    b_id = models.IntegerField()
    content = models.TextField()
    regdate = models.DateField()
    update_date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'reply'