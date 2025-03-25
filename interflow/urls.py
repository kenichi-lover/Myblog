from django.urls import path
from . import views
app_name = 'interflow'
urlpatterns = [

    path('<int:id>/', views.IndexView.as_view(), name='index'),


    path('page/',views.PageListView.as_view(),name='page_list'),

    path('page/<int:id>/',views.PageListView.as_view(),name='page_list'),

    path('publish/', views.publish_interflow, name='publish_interflow'),
    path('test/', views.test_view, name='test'),

]