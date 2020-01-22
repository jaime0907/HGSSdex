# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class ForthGen(models.Model):
    place = models.TextField(blank=True, null=True)
    dex = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    hg = models.IntegerField(blank=True, null=True)
    ss = models.IntegerField(blank=True, null=True)
    d = models.IntegerField(blank=True, null=True)
    pe = models.IntegerField(blank=True, null=True)
    pt = models.IntegerField(blank=True, null=True)
    method = models.CharField(max_length=45, blank=True, null=True)
    levelmin = models.IntegerField(blank=True, null=True)
    levelmax = models.IntegerField(blank=True, null=True)
    probdawn = models.IntegerField(blank=True, null=True)
    probday = models.IntegerField(blank=True, null=True)
    probnight = models.IntegerField(blank=True, null=True)
    specialprob = models.CharField(max_length=45, blank=True, null=True)
    subloc = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '4gen'


class Images(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'


class Locations(models.Model):
    id = models.IntegerField(primary_key=True)
    place = models.TextField(blank=True, null=True)
    dex = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    game = models.IntegerField(blank=True, null=True)
    method = models.CharField(max_length=45, blank=True, null=True)
    levelmin = models.IntegerField(blank=True, null=True)
    levelmax = models.IntegerField(blank=True, null=True)
    probdawn = models.IntegerField(blank=True, null=True)
    probday = models.IntegerField(blank=True, null=True)
    probnight = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations'


class Users(models.Model):
    username = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
