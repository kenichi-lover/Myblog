from django.urls import path
from . import views
app_name = 'article'
urlpatterns = [
    path('', views.home_view, name='home'),

    path('<int:id>/', views.publish_article, name='index'),
    path('page/', views.page_list, name='page_list'),
    path('page/<int:id>/', views.page_list, name='old_page_list'),

    path('test/', views.test_view, name='test'),

]