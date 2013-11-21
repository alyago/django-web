import random

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from serpng.articles.models import Article, Category
from jobs.translation_strings import translations

def category(request, category_slug):
    
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return HttpResponseRedirect(reverse('articles-url:index'))
    
    posts = list(Article.objects.filter(category=category))
    featured = []
    # Randomly choose 3 to be our "featured" articles
    while len(featured) < 3:
        featured.append(posts.pop(random.randrange(len(posts))))

    current_country_code = request.language_code.get_country_code()

    featured_posts = {}
    for post in featured:
        body = post.body
        featured_posts[post] = body[body.find("<p>")+3:] 

    return render(request,
        'articles/category.html', 
        {
            'category': category,
            'posts': posts,
            'featured_posts': featured_posts,
            'translations': translations,
            'current_country_code': current_country_code,
        })
