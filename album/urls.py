from django.urls import path
from . import views
app_name = 'album'
urlpatterns = [
path('', views.home_view, name='home'),
path('<int:id>/', views.IndexView.as_view(), {'page': 1}, name='index_page'),
path('<int:id>/<int:page>/', views.IndexView.as_view(), name='index_page'),
path('upload/', views.upload_photo_view, name='upload_photo'),
path('test/', views.test_view, name='test'),


]