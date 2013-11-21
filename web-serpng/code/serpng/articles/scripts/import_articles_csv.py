#!/usr/bin/env python
# encoding: utf-8
"""
import_articles_csv.py

Various importers for bringing data into the articles database from CSV, etc.

This script requires django-extensions in order to run. To install, activate
your employers virtual environment and run:

  pip install django-extensions

Then, add the following to your settings.py:

  'django_extensions'

Afterwards, you can run the script via:

  python manage.py runscript import_articles_csv

Copyright (c) 2013 Simply Hired, Inc. All rights reserved.
"""
import os
import unicodecsv
from datetime import date, timedelta

from django.template.defaultfilters import slugify

from articles.models import Category, Article


def get_path(filename):
    folder = os.path.dirname(__file__)
    return os.path.join(folder, filename)


class ArticleImporter(object):
    """Imports articles from CSV into the articles application."""

    def __init__(self, path_to_csv):
        """Initialize a new `ArticleImporter` instance."""
        today = date.today()
        days_since_last_monday = 7 if today.weekday() < 1 else today.weekday()
        self.post_date = date.today() - timedelta(days=days_since_last_monday)
        self.path_to_csv = path_to_csv

    def _category(self, category_title):
        """Get the `Category` instance with the given title."""
        category, created = Category.objects.get_or_create(
            slug=slugify(category_title),
            defaults={'title': category_title})
        if created:
            print "Created '%s' category" % category.title
        return category

    def _post_article(self, title, body_text, category, row_idx):
        """Post an article."""
        article, created = Article.objects.get_or_create(
            slug=slugify(title),
            defaults={'title': title,
                      'body': body_text,
                      'posted': self.post_date,
                      'category': category})
        if created:
            print "Created '%s' article" % title
        else:
            print "Article '%s' already exists" % title
            return
        if row_idx % 2 == 0:
            # Go a week back
            self.post_date = self.post_date = timedelta(days=7)

    def post_csv(self):
        """Post the rows in the CSV file and return the number of rows
        processed."""
        csv_row_idx = 2  # The Excel row number for debugging purposes.
        with open(self.path_to_csv, 'rU') as file_in:
            csv_file = unicodecsv.DictReader(file_in)
            for row in csv_file:
                category = self._category(row['category'])
                self._post_article(row['title'],
                                   row['body'],
                                   category,
                                   csv_row_idx)
                csv_row_idx += 1
        return csv_row_idx - 2


def run():  # pragma: no cover
    """Import the CSV file specified by `filename`"""
    filename = get_path('article_import_1.csv')
    ai = ArticleImporter(filename)
    rows = ai.post_csv()
    print '%d rows processed' % rows
