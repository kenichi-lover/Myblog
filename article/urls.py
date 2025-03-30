from django.urls import path
from . import views
app_name = 'article'
urlpatterns = [
    #path('', views.HomePageView.as_view(), name='home'),
    path('', views.HomePageView.as_view(), name='home'),

    path('<int:id>/', views.publish_article, name='index'),
    path('page/', views.PageListView.as_view(), name='page_list'),
    path('page/<int:id>/', views.PageListView.as_view(), name='old_page_list'),

    path('test/', views.test_view, name='test'),

]