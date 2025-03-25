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

    def get(self, request, id=None):
        if id is None:
            id = request.user.id

        album = AlbumInfo.objects.filter(user_id=id)
        tag = ArticleTag.objects.filter(user_id=id)
        user = MyUser.objects.filter(id=id).first()
        return render(request, 'account/index.html', {'album': album, 'tag': tag, 'user': user})


def register_view(request):
    if request.method == "POST":
        # 使用 RegisterForm 类（自定义的注册表单）创建一个表单实例。request.POST 将 POST 请求中的数据传递给表单，以便进行验证。
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 表单若有效，调用 form.save() 方法将表单数据保存到数据库中，创建一个新的用户帐户。
            form.save()
            return JsonResponse({"status": "success"})
        else:
            # form.errors.as_data() 将错误信息转换为 Python 字典，以便于打印。
            print(form.errors.as_data())
    else:
        # 如果请求方法不是 "POST"，则创建一个空的 RegisterForm 实例。
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})

def login_view(request):
    # 如果是 "POST"，则表示用户提交了登录表单。否则（通常是 "GET"），表示用户首次访问登录页面。
    if request.method == "POST":
        # 使用 AuthenticationForm 类（Django 内置的登录表单）创建一个表单实例。data=request.POST 将 POST 请求中的数据传递给表单，以便进行验证。
        form = AuthenticationForm(data=request.POST)
        print(form.errors)
        # 如果表单数据有效，则继续执行。
        if form.is_valid():
            print(form.cleaned_data)
            # 从验证后的表单数据中获取用户名和密码。
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 使用 authenticate() 函数（Django 内置的身份验证函数）验证用户名和密码。如果认证成功，authenticate() 返回一个 User 对象；否则，返回 None。
            user = authenticate(request, username=username, password=password)
            # 如果 authenticate() 返回了一个 User 对象，则调用 login() 函数（Django 内置的登录函数）将用户登录。
            if user is not None:
                login(request, user)
                return redirect('account:home')
            else:
                print("认证失败：用户名或密码错误")
        return render(request, 'account/login.html', {'form': form})
    else:
        # 如果请求方法不是 "POST"，则创建一个空的 AuthenticationForm 实例。
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})



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