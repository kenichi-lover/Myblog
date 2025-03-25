from django.http import HttpResponse
from django.views import View
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from album.models import AlbumInfo
from .forms import AlbumInfoForm


# Create your views here.
def home_view(request):
    return render(request, 'home.html')
class IndexView(LoginRequiredMixin,View):
    def get(self, request,id=None,page=1):
        if id is None:
            id = request.user.id
        # 获取所有图片信息
        album_list = AlbumInfo.objects.filter(user_id=id).order_by('id')
        # 创建分页器对象
        album_obj = Paginator(album_list, 3)
        # 获取当前页的数据
        try:
            pageinfo = album_obj.page(page) # 这行代码尝试获取指定页码page的数据。
        except PageNotAnInteger:   # 如果page不是一个整数，
            pageinfo = album_obj.page(1) # 将显示第一页的数据。
        except EmptyPage:  # 请求的页码超出了有效范围
            pageinfo = album_obj.page(album_obj.num_pages) # 显示最后一页的数据。
        return render(request, 'album/album_list.html', {'pageinfo':pageinfo, 'user':request.user})


@login_required
def upload_photo_view(request):
    if request.method == 'POST':
        form = AlbumInfoForm(request.POST, request.FILES)
        if form.is_valid():
            album_info = form.save(commit=False)
            album_info.user = request.user
            album_info.save()
            return redirect('album:index_page', id=request.user.id, page=1)  # 重定向到相册首页
    else:
        form = AlbumInfoForm()
    return render(request, 'album/album_upload.html', {'form': form})



def test_view(request):
    user_id = 1
    result = AlbumInfo.objects.filter(user_id=user_id).all()
    image = result[2]
    image.delete()
    print(result)

    return HttpResponse('成功')
