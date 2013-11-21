from django.db import models


class FormattedDescriptions(models.Model):
    description_id = models.IntegerField(db_column='id', primary_key=True)
    refindkey = models.CharField(max_length=40L, unique=True, db_column='refindKey', blank=True)  # Field name made lowercase.
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'FormattedDescriptions'
