# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class UpInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    mid = models.BigIntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    live_url = models.CharField(max_length=255, blank=True, null=True)
    fssl = models.IntegerField(blank=True, null=True)
    spsl = models.IntegerField(blank=True, null=True)
    ydl = models.IntegerField(blank=True, null=True)
    dzl = models.IntegerField(blank=True, null=True)
    bfl = models.IntegerField(blank=True, null=True)
    yn = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'up_info'


class Video(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    up_name = models.CharField(max_length=100, blank=True, null=True)
    mid = models.BigIntegerField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    bfl = models.IntegerField(blank=True, null=True)
    plsl = models.IntegerField(blank=True, null=True)
    dt = models.CharField(max_length=255, blank=True, null=True)
    length = models.CharField(max_length=255, blank=True, null=True)
    dmsl = models.IntegerField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    yn = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'video'
