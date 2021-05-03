# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Transazioni(models.Model):
    id_siamotrieste = models.PositiveIntegerField(unique=True, blank=True, null=True)
    id_utente = models.PositiveIntegerField()
    id_azienda = models.PositiveIntegerField()
    importo = models.FloatField()
    percentuale = models.FloatField()
    bricks = models.FloatField()
    district_utente = models.PositiveIntegerField()
    district_merchant = models.PositiveIntegerField()
    bricks_district_utente = models.FloatField()
    bricks_district_merchant = models.FloatField()
    id_trans_bosco = models.PositiveIntegerField()
    id_trans_discount = models.PositiveIntegerField()
    annullata = models.PositiveIntegerField()
    test = models.PositiveIntegerField()
    data = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transazioni'
