# http://djangosnippets.org/snippets/2687/

class ModelDatabaseRouter(object):
    """Routes databases."""

    def db_for_read(self, model, **hints):
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db

        return None

    def db_for_write(self, model, **hints):
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db

        return None

    def allow_syncdb(self, db, model):
        # Specify target database with field in_db in model's Meta class
        print "ModelDatabaseRouter saw db %s, model %s" % (str(db), str(model))
        if hasattr(model._meta, 'in_db'):
            if model._meta.in_db == db:
                return True
            else:
                return False
        else:
            # Random models that don't specify a database can only go to 'default'
            if db == 'default':
                return True
            else:
                return False
