from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View

from album.models import AlbumInfo
from article.models import ArticleTag
from .forms import RegisterForm

from .models import MyUser
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
def home_view(request):
    return render(request, 'home.html')
class IndexView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        album = AlbumInfo.objects.filter(user_id=user_id)
        tag = ArticleTag.objects.filter(user_id=user_id)
        user = MyUser.objects.filter(id=user_id).first()
        return render(request, 'account/index.html', {'album': album, 'tag': tag, 'user': user})

class RegisterView(View):  # 实现注册功能
    template_name = 'account/register.html'
    form_class = RegisterForm
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'account/login.html'
    form_class = AuthenticationForm
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                print('认证失败，用户名或密码错误')
        return render(request, self.template_name, {'form': form})




def logout_view(request):
    logout(request)
    messages.info(request, '您已安全退出系统')
    return redirect('account:home')



def test_view(request):
    user_list = MyUser.objects.all()
    name = MyUser.objects.filter(id=4)
    name.update(name='我是一只鱼',telephone=13888888888)
    for user in user_list:
        print(user)
    return HttpResponse('成功')