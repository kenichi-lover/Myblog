from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.core.paginator import Paginator, EmptyPage

from django.views.generic import ListView
from .models import ArticleInfo

from django.urls import reverse
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required
# Create your views here.


class HomePageView(ListView):
    model = ArticleInfo
    template_name = 'home.html'
    context_object_name = 'page_obj'
    paginate_by = 3

    def get_queryset(self): # 重写 get_queryset 方法:
        return ArticleInfo.objects.all().order_by('-created')

    def get_context_data(self, **kwargs): # 重写 get_context_data 方法.get_context_data 方法用于向模板传递额外的上下文变量.
        context = super().get_context_data(**kwargs) # 首先调用父类的 get_context_data

        # 获取查询集
        queryset = self.get_queryset()

        # 创建 Paginator 对象
        paginator = Paginator(queryset, self.paginate_by)

        # 获取页码
        page_number_str = self.request.GET.get('page')
        try:
            page_number = int(page_number_str) if page_number_str else 1
            page_obj = paginator.get_page(page_number)
        except (ValueError, TypeError):
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        # 将 page_obj 添加到上下文中
        context['page_obj'] = page_obj

        return context

class PageListView(ListView):
    model = ArticleInfo
    template_name = 'article/page_list.html'
    context_object_name = 'page_obj'
    paginate_by = 3
    ordering = ['-created']  # 按创建时间倒序排序

    def get(self, request, *args, **kwargs):
        # 处理重定向
        if 'id' in kwargs and kwargs['id'] is not None:
            return redirect(f'{reverse("page_list")}?page={kwargs["id"]}', permanent=True)

        return super().get(request, *args, **kwargs)

@login_required()
def publish_article(request,id=None):
    if id is not None:
        if request.method == "POST":
            form = ArticleForm(request.POST,request.FILES)
            if form.is_valid():
                article = form.save(commit=False)

                article.author_id = request.user.id
                article.save()
                form.save_m2m()  # 专门用于处理多对多（many-to-many，m2m）关系的数据保存。在 form.save() 方法之后调用，以确保模型的主要数据已保存到数据库。
                                 # 在使用 ModelForm 并且表单包含 m2m 字段时，必须这样做。
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

'''
ListView 的优点：

简洁： ListView 封装了许多底层细节，例如数据获取、分页和上下文传递。 这使得你的视图代码更简洁易懂。

自动化： ListView 自动处理许多常见的任务，例如创建 Paginator 对象、处理异常和将数据传递给模板。

可定制： 你仍然可以通过重写 get_queryset、get_context_data 和其他方法来定制 ListView 的行为。
4.代码高度集中，可读性好

当你需要超越 ListView 的默认行为时，你可以这样做：

重写 get_queryset 方法： 如果你需要自定义查询集，例如添加过滤条件、排序规则或联表查询，可以重写 get_queryset 方法。

重写 get_context_data 方法： 如果你需要向模板传递额外的上下文变量，可以重写 get_context_data 方法。 记住要调用 super().get_context_data(**kwargs)，以确保 ListView 的默认上下文变量也被传递给模板。

使用 render_to_response 方法： 如果你需要完全控制模板渲染过程，可以重写 render_to_response 方法。

记住：

对于简单的数据展示，Listview是一个非常有效的工具。但是，如果你需要控制每一个参数的传递，则需要显示传递。

总而言之，ListView 是一个非常有用的工具，但它并非适用于所有场景。 只要你理解它的工作方式，并根据需要进行定制，就可以充分发挥它的优势。

请不要因为一次不愉快的经历就放弃 ListView。 尝试更好地理解它，并在合适的场景中使用它，你可能会发现它是一个非常有用的工具。
'''
