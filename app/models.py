"""
Definition of models.
"""

from django.db import models

class Medication(models.Model):
	sponsorApplicant = models.CharField(max_length=50)
	productNo = models.CharField(max_length=3)
	form = models.CharField(max_length=255)
	dosage = models.CharField(max_length=240)
	productMktStatus = models.IntegerField()
	teCode = models.CharField(max_length=100)
	referenceDrug = models.BooleanField()
	drugName = models.CharField(max_length=125)
	activeIngred = models.CharField(max_length=255)
