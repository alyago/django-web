from django.db import models
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^serpng\.resume\.fields\.BlobField"])

class BlobField(models.Field):
    description = "Blob"
    def db_type(self):
        return 'MEDIUMBLOB'

