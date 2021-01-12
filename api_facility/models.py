from django.db import models

class Facility(models.Model):
    f_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=100)
    gu = models.CharField(max_length=45)
    address = models.CharField(max_length=200, blank=True, null=True)
    tel = models.CharField(max_length=45, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'facility'