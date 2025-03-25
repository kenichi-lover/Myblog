from django.contrib import admin
from .models import ArticleTag, ArticleInfo, Comment


# ArticleInfo 模型优化
class ArticleInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_short', 'content_preview', 'author_display')
    list_filter = ('created', 'article_tag')
    search_fields = ('title', 'content')
    date_hierarchy = 'created'

    def created_short(self, obj):
        return obj.created.strftime("%Y-%m-%d")

    created_short.short_description = '发布日期'

    def content_preview(self, obj):
        return f"{obj.content[:50]}..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = '内容摘要'

    def author_display(self, obj):
        return obj.author.username if obj.author else "未知作者"

    author_display.short_description = '作者'


# 其他模型增强
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'article_count')

    def article_count(self, obj):
        return obj.articles.count()

    article_count.short_description = '关联文章数'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenting_user', 'comment', 'created', 'text_short')
    list_filter = ('created',)
    raw_id_fields = ('comment',)

    def text_short(self, obj):
        return obj.comment.content[:50]


# 注册模型
admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(ArticleInfo, ArticleInfoAdmin)
admin.site.register(Comment, CommentAdmin)
