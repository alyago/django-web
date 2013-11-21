# Copyright (c) 2012, Simply Hired, Inc. All rights reserved.

"""Database Router"""


class SHRouter(object):

    def db_for_read(self, model, **hints):
        if model.__module__.startswith("autocomplete.models"):
            return 'autocomplete'
        else:
            None


class AllowSyncDBRouter(object):

    def allow_syncdb(self, db, model):

        if db == 'default' and model.__module__.startswith('django.contrib.sessions.models'):
            return True

        if db == 'resume' and (model.__module__.startswith("serpng.resume.models") or
                               model.__module__.startswith('south.')):
            return True

        return False
