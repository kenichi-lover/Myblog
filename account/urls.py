from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('<int:id>/', views.IndexView.as_view(), name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),


    path('test/', views.test_view, name='test'),
    path('logout/', views.logout_view, name='logout'),





]