from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from serpng.articles.models import Article, Category
from jobs.translation_strings import translations

# a catch-all for employer pages
def redirect_to_default(request):
    return HttpResponseRedirect(reverse('articles-url:index'))

def index(request):

    current_country_code = request.language_code.get_country_code()
    
    categories = Category.objects.all()
    article_data = {}
    for cat in categories:
        article_data[cat] = Article.objects.filter(category=cat).order_by('?')[:5]

    return render(request, 
                'articles/index.html', 
                {
                    'article_data': article_data,
                    'translations': translations,
                    'current_country_code': current_country_code,
                })
