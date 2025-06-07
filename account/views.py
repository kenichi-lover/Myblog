from django.contrib.auth import login,logout

from django.http import HttpResponse
from django.shortcuts import render,redirect

from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView

from album.models import AlbumInfo
from article.models import ArticleTag
from .forms import RegisterForm,MyAuthenticationForm

from .models import MyUser
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
def home_view(request):
    return render(request, 'home.html')
class IndexView(LoginRequiredMixin, View):  #  展示登录信息

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        album = AlbumInfo.objects.filter(user_id=user_id)
        tag = ArticleTag.objects.filter(user_id=user_id)
        user = MyUser.objects.filter(id=user_id).first()
        return render(request, 'account/index.html', {'album': album, 'tag': tag, 'user': user})

class RegisterView(CreateView):  # 实现注册功能
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('account:home')
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)



class LoginView(View):  # 实现登录功能
    template_name = 'account/login.html'
    form_class = MyAuthenticationForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('article:home')

        return render(request,self.template_name,{'form':self.form_class(request)})


    def post(self, request):
        form = self.form_class(request,data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('article:home')
        return render(request,self.template_name,{'form':form})

def logout_view(request):
    logout(request)
    messages.info(request, '您已安全退出系统')
    return redirect('article:home')



def test_view(request):

    user = MyUser.objects.filter(id=4)


    print(user)
    return HttpResponse('成功')
'''
LoginRequiredMixin: 这是 Django 提供的一个非常常用的 Mixin（混入类）。它的作用就是：
如果用户没有登录，它会自动将用户重定向到 settings.LOGIN_URL 指定的登录页面。
如果用户已经登录，它才会允许 get 或 post 等方法继续执行，从而渲染视图内容。
'''
