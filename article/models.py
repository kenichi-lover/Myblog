from django.utils import timezone

from django.db import models
from account.models import MyUser

# Create your models here.
class ArticleTag(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=120,verbose_name='标签')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,verbose_name='用户')

    def __str__(self):
        return self.tag
    class Meta:
        db_table = 'article_tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name

class ArticleInfo(models.Model):
    author = models.ForeignKey(MyUser,on_delete=models.CASCADE,verbose_name='用户')
    title = models.CharField(max_length=200,verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    article_photo = models.ImageField(verbose_name='头像',blank=True,upload_to='media/image/')
    created = models.DateTimeField(verbose_name='创建时间',default=timezone.now)
    updated = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    article_tag = models.ManyToManyField(ArticleTag,blank=True,related_name='articles',verbose_name='文章标签')

    def __str__(self):
        return f"title:{self.title},author:{self.author}"
    class Meta:
        db_table = 'article_info'
        verbose_name = '标题'
        verbose_name_plural = verbose_name

class Comment(models.Model):
    comment = models.ForeignKey(ArticleInfo,on_delete=models.CASCADE,verbose_name='所属文章')
    commenting_user = models.CharField(max_length=100,verbose_name='评论用户')
    content = models.TextField(verbose_name='评论内容')
    created = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return self.comment.title
    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
