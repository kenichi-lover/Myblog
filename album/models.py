from django.db import models
from account.models import MyUser
# Create your models here.
class AlbumInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField(max_length=30,blank=True,verbose_name='标题')
    introduce = models.CharField(max_length=100,blank=True,verbose_name='描述')
    photo = models.ImageField(verbose_name='图片',blank=True,upload_to='image/')

    def __str__(self):
        return f"title:{self.title},author:{self.user}"
    class Meta:
        db_table = 'album_info'
        verbose_name = '图片信息'
        verbose_name_plural = verbose_name

