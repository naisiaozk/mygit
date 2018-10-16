from io import BytesIO
import uuid

from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import render,redirect,reverse
# from django.core.cache import cache
from django.core.paginator import Paginator
from django.conf import settings

from . import models
from . import utils


def index(request):
    articles = models.Article.objects.all()
    return render(request,"blog/index.html",{"articles": articles})

    # 使用Django自带的分页器，首先构建一个Paginator对象
    paginator = Paginator(articles, pageSize)
    page = paginator.page(pageNow)

    return render(request, "blog/article_list.html", {"page": page, "pageSize": pageSize})


def add_user(request):
    # 首先需要接受页面传递过来的参数
    username = "lisi"
    age = 16
    password = "123456"
    email = "110@qq.com"
    try:
        # 第一种方式，使用类方法的方式完成数据的操作
        # user = models.User.create_user(username=username, password=password, age=age, email=email)
        # user.save()

        # 第三种，使用面向过程的方式实现
        # 因为我们model类继承了Model类，在Model类中有大量方法和属性
        # user = models.User(username=username, password=password, age=age, email=email)
        # user.save()

        user = models.User.um.add_user(username=username, password=password, age=age, email=email)
        print(user.id , user.username, user.password, user.email)

        return HttpResponse("<h2>用户添加成功！！！</h2>")
    except:
        return HttpResponse("<h2>对不起，用户添加失败！！！</h2>")


def delete_user(request):
    pass


def list_user(request):
    # users = models.User.um.all()
    # users = models.User.objects.all()
    pass


def login(request):
    """
       登录的视图函数，完成用户登录功能
       :param request: 请求头对象
       :return:
       """
    if request.method == "GET":
        return render(request, "blog/login.html", {"msg": "请登录"})
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # TODO 将来需要完善验证码
        code = request.POST["code"]
        mycode = request.session["code"]
        if code.upper() != mycode.upper():
            return render(request, "blog/login.html", {"msg": "验证码错误，请重新输入！！"})
        try:
            user = models.User.objects.get(username=username, password=password)
            # 使用session来记录登录用户的信息
            request.session["loginUser"] = user
            return redirect(reverse("blog:index"))
            response.set_cookie("username",user.name,max_age=3600*24*14)
            return response
        except:
            return render(request, "blog/login.html", {"msg": "登录失败，请重新登录！！"})
    # return render(request, "blog/login.html", {})


def register(request):
    if request.method == "GET":
        return render(request, "blog/register.html", {"msg": "请认真填写如下选项"})
    elif request.method == "POST":
        # 接受参数
        try:
            username = request.POST["username"].strip()
            password = request.POST.get("password").strip()  # .getlist()
            confirmpwd = request.POST.get("confirmpwd").strip()
            age = request.POST.get("age",None)
            nickname = request.POST.get("nickname", None)
            email = request.POST.get("email", None)
            birthday = request.POST.get("birthday", None)
            gender = request.POST.get("gender", None)
            avatar = request.FILES.get("avatar",'static/img/banel/default.png')

            code = request.POST['code']

            mycode = request.session["code"]
            if code.upper() != mycode.upper():
                return render(request, "blog/register.html", {"msg": "验证码错误，请重新输入！！"})

            # # 删除session中验证码
            # del request.session["code"]

            # 数据校验
            if len(username) < 1:
                return render(request, "blog/register.html", {"msg": "用户名称不能为空！！"})
            if len(password) < 6:
                return render(request, "blog/register.html", {"msg": "密码长度不能小于6位！！"})
            if password != confirmpwd:
                return render(request, "blog/register.html", {"msg": "两次密码不一致！！"})
            # 用户名称是否重复
            try:
                user = models.User.objects.get(username=username)
                return render(request, "blog/register.html", {"msg": "该用户名称已经存在，请重新填写！！"})
            except:
                # 保存数据
                user = models.User(username=username, password=password, age=age, nickname=nickname, email=email)
                user.save()
                return render(request, "blog/login.html", {"msg": "恭喜您，注册成功！！"})
                #保存数据
                try:
                    avatar = request.FILES['avatar']
                    #保存图片
                    path = "static/img/headers/" + uuid.uuid4().hex + avatar.name
                    with open(path, "wb") as f:
                        for file in avatar.chunks():
                            f.write(file)
                    user = models.User(name=username, password=password, nickname=nickname, header=avatar)
                    user.save()
                    return render(request, "blog/add_user.html", {"msg": "恭喜您，注册成功！！"})
                except Exception as e:
                    print(e)
                    user = models.User(name=username, password=password, nickname=nickname)
                    user.save()
                    return render(request, "blog/add_user.html", {"msg": "恭喜您，注册成功！！"})
        except:
            return render(request, "blog/register.html", {"msg": "对不起，用户名称不能为空！！"})
    # return render(request, "blog/register.html", {})



def code(request):
    img, code = utils.create_code()
    # 首先需要将code保存到session中
    request.session['code'] = code
    # 返回图片
    file = BytesIO()
    img.save(file, 'PNG')

    return HttpResponse(file.getvalue(), "image/png")


def article_publish(request):
    if request.method == "GET":
        return render(request, "blog/article_publish.html", {"msg": "请认真填写如下选项"})
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        author = request.session["loginUser"]

        # 验证
        article = models.Article(title=title, content=content, author=author)
        article.save()
        return redirect(reverse("blog:show_article", kwargs={"a_id": article.id}))


def show_article(request,a_id):
    at = models.Article.objects.get(pk=a_id)
    return render(request, "blog/show_article.html", {"article": at})


def article_update(request,a_id):
    at = models.Article.objects.get(pk=a_id)
    if request.method == "GET":
        return render(request, "blog/article_update.html", {"article": at})
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        at.title = title
        at.content = content
        at.save()
        return redirect(reverse("blog:show_arcticle", kwargs={"a_id": a_id}))


def article_list(request):
    articles = models.Article.objects.all()
    return render(request, "blog/article_list.html", {"articles": articles})

    # 使用Django自带的分页器，首先构建一个Paginator对象
    paginator = Paginator(articles, pageSize)
    page = paginator.page(pageNow)

    return render(request, "blog/index1.html", {"page": page, "pageSize": pageSize})