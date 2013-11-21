from django.db import models

class Locations(models.Model):
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	popularity = models.DecimalField(max_digits=8,decimal_places=4)	
	msacode = models.CharField(max_length=16)

class Keywords(models.Model):
	keyword = models.CharField(max_length=50,primary_key=True)
	popularity = models.IntegerField(max_length=11)
