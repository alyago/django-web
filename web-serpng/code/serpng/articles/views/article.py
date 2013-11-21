from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from serpng.articles.models import Article, Category
from jobs.translation_strings import translations

def article(request, article_slug):

    try:
        article = Article.objects.get(slug=article_slug)
    except Article.DoesNotExist:
        return HttpResponseRedirect(reverse('articles-url:index'))

    current_country_code = request.language_code.get_country_code()
    categories = Category.objects.all()
    
    return render(request,
                'articles/article.html', 
                {
                    'article': article,
                    'translations': translations,
                    'current_country_code': current_country_code,
                    'categories': categories,
                })
