from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class MyUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True,verbose_name='姓名') # 一定要设置blank=True，不然注册页面一定要包含此字段
    telephone = models.CharField(max_length=11,blank=True,verbose_name='电话',default='暂时没有') # 同上
    introduce = models.TextField('简介', default='暂无介绍')


    def __str__(self):
        return f"name: {self.name}, telephone: {self.telephone}"
    class Meta:
        db_table = 'myuser'
        verbose_name = '用户'
        verbose_name_plural = verbose_name