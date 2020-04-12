from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from app01 import myforms
from app01 import models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count,F
from django.db.models.functions import TruncMonth
from django.utils.safestring import mark_safe
# Create your views here.


def register(request):
    form_obj = myforms.MyRegForm()
    if request.method == 'POST':
        back_dic = {'code':100,'msg':''}
        # 校验用户信息是否合法
        form_obj = myforms.MyRegForm(request.POST)
        if form_obj.is_valid():
            clean_data = form_obj.cleaned_data  # clean_data = {'username':'','password':'','confirm_password':'','email':''}
            clean_data.pop('confirm_password')  # clean_data = {'username':'','password':'','email':''}
            # 手动获取用户头像
            user_file = request.FILES.get('myfile')
            if user_file:  # 一定要判断用户是否传头像了 如果传了才往字典里面添加  没传不用添加 因为有默认
                clean_data['avatar'] = user_file
            # 创建数据
            models.UserInfo.objects.create_user(**clean_data)
            back_dic['msg'] = '注册成功'
            back_dic['url'] = '/login/'
        else:
            back_dic['code'] = 101
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)

    return render(request,'register.html',locals())


def login(request):
    if request.method == 'POST':
        back_dic = {'code':100,'msg':''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        # 1.先校验用户输入的验证码是否正确  忽略大小写校验 内部统一转大写或者小写比较
        if request.session.get('code').upper() == code.upper():
            # 2.数据库校验用户名和密码是否正确
            user_obj = auth.authenticate(username=username,password=password)
            if user_obj:
                # 3.保存用户登录状态
                auth.login(request,user_obj)
                back_dic['msg'] = '登录成功'
                back_dic['url'] = '/home/'
            else:
                back_dic['code'] = 101
                back_dic['msg'] = '用户名或密码错误'
        else:
            back_dic['code'] = 102
            back_dic['msg'] = '验证码错误'
        return JsonResponse(back_dic)
    return render(request,'login.html')

from PIL import Image,ImageDraw,ImageFont
"""
Image  生成图片的
ImageDraw  在图片上写东西的
ImageFont  控制字体样式的
"""
import random
from io import BytesIO,StringIO
"""
io是一个内存管理器模块
BytesIO  能够帮你存储数据 二级制格式
StringIO 能够帮你存储数据 字符串格式
"""

def get_random():
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)

# 验证码相关
def get_code(request):
    # 推导步骤1:直接将本地已经存图片的以二进制方式读取发送
    # with open(r'D:\python脱产10期视频\BBS\avatar\222.jpg','rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 推导步骤2:能够产生任何多张的图片的方法
    # img_obj = Image.new('RGB',(35,360),'green')
    # img_obj = Image.new('RGB',(35,360),get_random())
    # # 先以文件的形式保存下来
    # with open('xxx','wb') as f:
    #     img_obj.save(f,'png')
    # # 然后再打开这个文件发送
    # with open('xxx','rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 推导步骤3:需要找一个能够临时存储文件的地方  避免频繁文件读写操作
    # img_obj = Image.new('RGB', (35, 360), get_random())
    # io_obj = BytesIO()  # 实例化产生一个内存管理对象  你可以把它当成文件句柄
    # img_obj.save(io_obj,'png')
    # return HttpResponse(io_obj.getvalue())  # 从内存对象中获取二级制的图片数据
    # 推导步骤4:在产生的图片上 写验证码
    img_obj = Image.new('RGB', (360,35), get_random())
    img_draw = ImageDraw.Draw(img_obj)  # 生成一个可以在图片上写字的画笔对象
    img_font = ImageFont.truetype('static/font/222.ttf',30)  # 字体样式 及 大小
    io_obj = BytesIO()
    # 图片验证码 一般都是有 数字  大写字母  小写字母
    # 五位  每一位都可以 数字或大写字母或小写字母
    code = ''
    for i in range(5):
        upper_str = chr(random.randint(65,90))
        low_str = chr(random.randint(97,122))
        random_int = str(random.randint(0,9))
        # 随机取一个
        temp_code = random.choice([upper_str,low_str,random_int])
        # 朝图片上写
        img_draw.text((70+i*45,0),temp_code,get_random(),font=img_font)
        code += temp_code
    print(code)
    # 将产生的随机验证码 存入session中 以便后续其他视图函数获取 校验验证码
    request.session['code'] = code
    img_obj.save(io_obj,'png')
    return HttpResponse(io_obj.getvalue())


def home(request):
    # 获取网站所有的文章 展会到前端
    article_list = models.Article.objects.all()
    # 如果文章数目比较多  你应该做分页处理

    return render(request,'home.html',locals())

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/login/')

@login_required
def set_password(request):
    if request.is_ajax():
        back_dic = {'code':100,'msg':''}
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        is_right = request.user.check_password(old_password)
        if is_right:
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                back_dic['msg'] = '修改成功'
                back_dic['url'] = '/login/'
            else:
                back_dic['code'] = 102
                back_dic['msg'] = '两次密码不一致'
        else:
            back_dic['code'] = 101
            back_dic['msg'] = '原密码错误'

        return JsonResponse(back_dic)


def site(request,username,**kwargs):
    # 先获取用户用户名 查看是否存在
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        # 如果用户不存在 应该返回一个404页面
        return render(request,'errors.html')
    # 获取该用户的个人站点
    blog = user_obj.blog
    # 查询当前这个人的所有的文章
    article_list = models.Article.objects.filter(blog=blog)
    """侧边栏筛选功能:就是对当前用户所有的文章 再进行一次筛选"""
    if kwargs:
        condition = kwargs.get('condition')  # tag/category/archive
        param = kwargs.get('param')  # 1/1/2019-1
        if condition == 'category':
            article_list = article_list.filter(category_id=param)
        elif condition == 'tag':
            article_list = article_list.filter(tag__id=param)
        else:
            year,month = param.split('-')
            article_list = article_list.filter(create_time__year=year,create_time__month=month)
    # 查询当前用户每一个分类下的文章数
    # category_menu = models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values_list('name', 'c','pk')
    # # print(category_menu)
    # # 查询每一个分类下的文章数
    # # res = models.Category.objects.annotate(c=Count('article')).values('name','c')
    # # print(res)
    # # 查询当前用户每一个标签下的文章数
    # tag_menu = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values_list('name','c','pk')
    # # print(tag_menu)
    # date_menu = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values('month').annotate(c=Count('pk')).values_list('month','c')
    # # print(date_menu)
    return render(request,'site.html',locals())


def article_detail(request,username,article_id):
    # 先获取用户用户名 查看是否存在
    user_obj = models.UserInfo.objects.filter(username=username).first()
    if not user_obj:
        # 如果用户不存在 应该返回一个404页面
        return render(request, 'errors.html')
    blog = user_obj.blog
    # 根据文章id 查询出对应的文章 展示到前端 即可
    article_obj = models.Article.objects.filter(pk=article_id,blog=blog).first()
    comment_list = models.Comment.objects.filter(article=article_obj)
    return render(request,'article_detail.html',locals())
import json
# 仅仅只是处理ajax请求点赞点踩逻辑
def up_or_down(request):
    if request.is_ajax():
        back_dic = {'code':100,'msg':''}
        # 1 先校验用户是否登录
        if request.user.is_authenticated():
            # 获取必要的数据
            article_id = request.POST.get("article_id")
            is_up = request.POST.get('is_up')
            # 将字符串形式的js布尔值转换成后端python布尔值
            is_up = json.loads(is_up)
            # 2 校验当前文章是否是当前用户自己写的
            article_obj = models.Article.objects.filter(pk=article_id).first()
            if not article_obj.blog.userinfo == request.user:
                # 3 校验当前用户是否已经给当前文章点过赞或踩
                is_click = models.UpAndDown.objects.filter(article=article_obj,user=request.user)
                if not is_click:
                    # 4 操作数据库 记录数据  在记录的时候 需要做到文章表里的普通字段跟点赞点踩数据同步  并且区分是点赞还是点踩
                    if is_up:
                        # 如果是赞 先把文章表里面的普通点赞字段加1
                        models.Article.objects.filter(pk=article_id).update(up_num = F('up_num') + 1)
                        back_dic['msg'] = '点赞成功'
                    else:
                        # 如果是踩 先把文章表里面的普通点踩字段加1
                        models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                        back_dic['msg'] = '点踩成功'
                    # 操作点赞点踩表  存实际数据
                    models.UpAndDown.objects.create(user=request.user,article=article_obj,is_up=is_up)
                else:
                    back_dic['code'] = 101
                    back_dic['msg'] = '你已经点过了'
            else:
                back_dic['code'] = 102
                back_dic['msg'] = '你个臭不要脸的，不能点自己的！'
        else:
            back_dic['code'] = 103
            back_dic['msg'] = mark_safe('请先<a href="/login/">登录</a>')
        return JsonResponse(back_dic)

"""
事务
"""


from django.db import transaction

def comment(request):
    if request.is_ajax():
        back_dic = {'code':100,'msg':''}
        # 前端虽然更具用户是否登录展示评论框 但是后端最好再校验一次用户是否登录
        if request.user.is_authenticated():
            content = request.POST.get('content')
            article_id = request.POST.get('article_id')
            parentId = request.POST.get('parentId')
            # 评论表  文章评论数普通字段 同步
            with transaction.atomic():
                models.Comment.objects.create(user=request.user,article_id=article_id,content=content,parent_id=parentId)
                models.Article.objects.filter(pk=article_id).update(comment_num = F('comment_num') + 1)
            back_dic['msg'] = '评论成功'
        else:
            back_dic['code'] = 101
            back_dic['msg'] = mark_safe('请先<a href="/login/">登录</a>')
        return JsonResponse(back_dic)

from utils.mypage import Pagination
@login_required
def backend(request):
    article_list = models.Article.objects.filter(blog=request.user.blog)
    page_obj = Pagination(current_page=request.GET.get('page',1),all_count=article_list.count(),per_page_num=10)
    page_queryset = article_list[page_obj.start:page_obj.end]
    return render(request,'backend/backend.html',locals())


from bs4 import BeautifulSoup

@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.getlist('tag')
        category_id = request.POST.get('category')
        # 麻瓜式做法  直接对content窃取150
        #  1 先生成一个BeautifulSoup对象
        soup = BeautifulSoup(content,'html.parser')
        for tag in soup.find_all():
            # 针对script标签 应该直接删除
            # print(tag.name)  # 获取当前html页面所有的标签
            if tag.name == 'script':
                tag.decompose()  # 将符合条件的标签删除

        # 文章简介应该是150个文本内容
        desc = soup.text[0:150]
        # desc = content[0:150]
        article_obj = models.Article.objects.create(title=title,desc=desc,content=str(soup),category_id=category_id,blog=request.user.blog)
        # 一个个的添加
        b_list = []
        for tag_id in tags:
            b_list.append(models.Article2Tag(article=article_obj,tag_id=tag_id))
        models.Article2Tag.objects.bulk_create(b_list)
        return redirect('/backend/')

    tag_list = models.Tag.objects.filter(blog=request.user.blog)
    category_list = models.Category.objects.filter(blog=request.user.blog)
    return render(request,'backend/add_article.html',locals())


import os
from BBS import settings

def upload_img(request):
    # 接收用户写文章传的所有的图片资源
    if request.method == 'POST':
        file_obj = request.FILES.get('imgFile')
        # 要将文件存入media文件下一个专门用来存储文章图片的文件夹(article_img)
        # 1 手动先拼接出图片所在的文件件路径
        base_path = os.path.join(settings.BASE_DIR,'media','article_img')
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        # 2 手动拼接文件的具体路径
        file_path = os.path.join(base_path,file_obj.name)
        # 3 文件操作
        with open(file_path,'wb') as f:
            for line in file_obj:
                f.write(line)
        """
        //成功时
            {
                    "error" : 0,
                    "url" : "http://www.example.com/path/to/file.ext"
            }
            //失败时
            {
                    "error" : 1,
                    "message" : "错误信息"
            }
        """
        back_dic = {
            'error':0,
            'url':'/media/article_img/%s'%file_obj.name
        }
        return JsonResponse(back_dic)


def edit_avatar(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('myfile')
        if file_obj:
            # models.UserInfo.objects.filter(pk=request.user.pk).update(avatar=file_obj)
            # queryset更新方法修改头像的时候 不会自动加avatar前缀
            # 你可以手动通过文件操作 写入文件  然后给avatar传一个手动拼接好的路径

            request.user.avatar = file_obj
            request.user.save()
        return redirect('/%s/'%request.user.username)
    return render(request,'edit_avatar1.html')
