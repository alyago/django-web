from django.conf.urls import patterns, url
from articles import views

urlpatterns = patterns( '',
    # Directory/Index/Browse tab
    url(r'^index.html$', views.index, name='index'),
   
    # Browse a category 
    url(r'^cat-(?P<category_slug>.+)$', views.category, name='category'),
   
    # Read an article
    url(r'^post-(?P<article_slug>.+)$', views.article, name='article'),

    # a catch-all for article pages
    url(r'.*', views.redirect_to_default),
)

