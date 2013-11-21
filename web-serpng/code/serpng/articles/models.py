"""
models.py

Django models for evergreen articles app.

Copyright (c) 2013 Simply Hired, Inc. All rights reserved.
"""
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
     

class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateField(db_index=True, auto_now_add=True)
    category = models.ForeignKey(Category, related_name='articles')

