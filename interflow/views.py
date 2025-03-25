
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Board
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InterflowInfoForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.views.generic import ListView


class IndexView(LoginRequiredMixin,View):
    def get(self, request,id=None):
        if id is not None:
            inter_flows = Board.objects.all()
        else:
            inter_flows = Board.objects.filter(user_id=id)
        interflow_list = Board.objects.all().order_by('-created')
        form = InterflowInfoForm()
        context = {'inter_flows':inter_flows, 'interflow_list':interflow_list, 'form':form}
        return render(request,'interflow/index.html',context)
    def post(self, request):
        form = InterflowInfoForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            board.save()
            return redirect('interflow:page_list')
        inter_flows = Board.objects.all()
        interflow_list = Board.objects.all().order_by('-created')
        context = {
            'inter_flows':inter_flows,
            'interflow_list':interflow_list,
            'form':form,
        }
        return render(request, 'interflow/index.html', context)

class PageListView(ListView):
    model = Board  # 指定模型
    template_name = 'interflow/interflow_detail.html'  # 指定模板
    context_object_name = 'page_obj'  # 指定传递给模板的变量名
    ordering = ['-created']  # 指定排序方式
    paginate_by = 3  # 指定每页显示的数量

    def get_queryset(self):
        queryset = Board.objects.all().order_by('-created')
        # 获取 URL 中的 id 参数
        id_param = self.request.GET.get('id')

        # 如果存在 id 参数，则进行过滤
        if id_param:
            try:
                id_value = int(id_param)
                queryset = queryset.filter(id=id_value)
            except ValueError:
                # 处理无效的 id 参数，例如显示所有留言或者返回错误信息
                pass  # 这里选择忽略无效的 id 参数，显示所有留言

        # 获取当前用户
        # user = self.request.user
        # if user.is_authenticated:
        #     queryset = queryset.filter(user=user) #根据用户进行过滤
        # else:
        #     queryset = queryset.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()  # 获取过滤后的 queryset
        paginator = Paginator(queryset, self.paginate_by)  # 创建 Paginator 对象
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['total_count'] = queryset.count() # 使用过滤后的queryset
        context['num_pages'] = paginator.num_pages  # 将 num_pages 添加到 context 中
        context['page_obj'] = page_obj # 把page_obj放进去，否则分页信息获取不到。
        return context

@login_required()
def publish_interflow(request):
    if request.method == "POST":
        form = InterflowInfoForm(request.POST,request.FILES)
        if form.is_valid():
            interflow = form.save(commit=False)

            interflow.user_id = request.user.id
            interflow.save()
            form.save_m2m()
            return redirect('interflow:page_list')
    else:
        form = InterflowInfoForm()
    return render(request,'interflow/index.html', {'form': form})

def test_view(request):
    inter_flows = Board.objects.count()
    pages = Board.objects.all().order_by('-created')
    paginator = Paginator(pages, 3)
    num_pages = paginator.num_pages
    print(num_pages,inter_flows)
    return HttpResponse('成功')


