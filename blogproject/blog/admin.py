from django.contrib import admin
from django.core.cache import cache

from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    # 列表展示
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    # 表单展示
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        # 当前登录用户
        obj.author = request.user
        super().save_model(request, obj, form, change)
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        """ 重写delete_model """
        # 删除表中的数据时调用
        super().delete_model(request, obj)
        # 清空缓存,key 是键名，之前缓存的是哪个就填哪个
        cache.delete('index_page_data')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
