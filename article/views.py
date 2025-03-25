from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage
from .models import ArticleInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def home_view(request):
    page_number_str = request.GET.get('page')
    article = ArticleInfo.objects.all().order_by('-created')
    paginator = Paginator(article, 3)
    try:
        page_number = int(page_number_str) if page_number_str else 1
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'home.html', context)


class IndexView(LoginRequiredMixin,View):

    def get(self, request ,id=None):
        if id is None:
            diaries = ArticleInfo.objects.all()
        else:
            diaries = ArticleInfo.objects.filter(author_id=id)
        article_list = ArticleInfo.objects.all().order_by('-created')[:5]

        context = {
            'diaries': diaries,
            'article_list': article_list
        }
        return render(request, 'article/index.html', context)


def page_list(request,id=None):
    if id :
        return redirect(f'{reverse("page_list")}?page={id}',
                        permanent=True)

    page_number_str = request.GET.get('page')
    pages = ArticleInfo.objects.all().order_by('-created')
    paginator = Paginator(pages, 3)
    try:
        page_number = int(page_number_str) if page_number_str else 1
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, 'article/page_list.html', {'page_obj': page_obj})

@login_required()
def publish_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            article = form.save(commit=False)

            article.author_id = request.user.id
            article.save()
            form.save_m2m()
            return redirect('article:home')
    else:
        form = ArticleForm()
    return render(request,'article/index.html', {'form': form})


def test_view(request):
    article_list = ArticleInfo.objects.all().order_by('-created')[:5]
    for article in article_list:
        print(article.title,article.author)
    articles_to_delete = ArticleInfo.objects.filter(title="LibreOffice: 自由免费的全能办公套件", author__name="袁圆")
    first_article = articles_to_delete.first()
    first_article.delete()
    return HttpResponse('成功')
