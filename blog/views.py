
# Create your views here.
from django.http import HttpResponse
from .models import Article

def article_list(request):
    articles = Article.objects.all()
    return HttpResponse(articles)
