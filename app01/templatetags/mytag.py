from django import template
from app01 import models
from django.db.models import Count
from django.db.models.functions import TruncMonth
register = template.Library()


@register.inclusion_tag('left_menu.html')
def left_menu(username):
    # 先获取用户用户名 查看是否存在
    user_obj = models.UserInfo.objects.filter(username=username).first()
    # 获取该用户的个人站点
    blog = user_obj.blog
    # 查询当前用户每一个分类下的文章数
    category_menu = models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values_list('name', 'c',
                                                                                                       'pk')
    # print(category_menu)
    # 查询每一个分类下的文章数
    # res = models.Category.objects.annotate(c=Count('article')).values('name','c')
    # print(res)
    # 查询当前用户每一个标签下的文章数
    tag_menu = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values_list('name', 'c', 'pk')
    # print(tag_menu)
    date_menu = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values(
        'month').annotate(c=Count('pk')).values_list('month', 'c')
    # print(date_menu)
    return locals()