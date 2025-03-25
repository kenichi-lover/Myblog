from django.db import models
from account.models import MyUser
from django.utils import timezone
# Create your models here.
class Board(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,verbose_name='留言用户')
    email = models.CharField(max_length=50,verbose_name='邮箱地址')
    content = models.CharField(max_length=100,verbose_name='留言内容')
    created = models.DateTimeField(default=timezone.now,verbose_name='创建时间')
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,verbose_name='用户')

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'board'
        verbose_name = '留言板'
        verbose_name_plural = verbose_name