
class ArticlesRouter(object):
    """
    A router to control all database operations on models in the articles app.
    
    Add to settings.py of your site:
    DATABASE_ROUTERS = ['articles.routers.ArticlesRouter']
    """
    def __init__(self):
        self.db = 'articles'
        self.app_label = 'articles'

    def db_for_read(self, model, **hints):
        """
        Attempts to read articles models go to emp_db.
        """
        if model._meta.app_label == self.app_label:
            return self.db
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write articles models go to emp_db.
        """
        if model._meta.app_label == self.app_label:
            return self.db
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation if both models are in articles app.
        """
        if obj1._meta.app_label == self.app_label and obj2._meta.app_label == self.app_label:
            return True

        # No opinion if both models are not in articles app.
        elif self.app_label not in [obj1._meta.app_label, obj2._meta.app_label]:
            return None

        # Disallow if one in articles and the other not.
        else:
            return False

    def allow_syncdb(self, db, model):
        """
        articles app models appear only in emp_db
        """
        if db == self.db and model._meta.app_label == self.app_label:
            return True
        elif db != self.db and model._meta.app_label != self.app_label:
            return None
        else:
            return False
