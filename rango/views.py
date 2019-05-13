from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from rango.form import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page


def index(request):
    # request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context = {'categories': category_list, 'pages': page_list}

    # 调用处理 cookie 的辅助函数
    visitor_cookie_handler(request)
    context['visits'] = request.session['visits']

    # 提前获取 response 对象，以便添加 cookie
    response = render(request, 'rango/index.html', context=context)

    # 返回response对象,更新目标cookie
    return response


def about(request):
    # if request.session.test_cookie_worked():
    #     print("TEST COOKIE WORKED!")
    #     request.session.delete_test_cookie()
    print(request.session.session_key)
    context = {
        'MEDIA_URL': '/media/',
    }
    return render(request, 'rango/about.html', context=context)


def show_category(request, category_name_slug):
    context = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by("-views")[:5]
        context['pages'] = pages
        context['category'] = category
    except Category.DoesNotExist:
        context['pages'] = None
        context['category'] = None
    return render(request, 'rango/category.html', context)


def add_category(request):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return input(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
            else:
                print(form.errors)
    context = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # 把UserForm中的数据存入数据库
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # 处理UserProfile实例
            # 因为要自行处理user属性,所以设定commit=False,延迟保存模型，以防出现完整性问题
            profile = profile_form.save(commit=False)
            profile.user = user

            # 用户提供头像？
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            # 注册成功
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # 不是POST请求，渲染两个Form实例
        # 表单为空,待用户填写
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                  'rango/register.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form,
                      'registered': registered
                  })


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # 账户是否激活，可能被禁用
            if user.is_active:
                # 登入有效账户
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("该账户未激活")
        else:
            # 提供的登录凭据有误，无法登陆
            print("Invalid login details:{0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    # 只有已登录的用户才能访问这个接口
    # 用户退出
    logout(request)

    # 把用户带回首页
    return HttpResponseRedirect(reverse('index'))


def visitor_cookie_handler_old(request, response):
    # 获取网站的访问次数
    visits = int(request.COOKIES.get('visits', '1'))

    # 获取最后访问时间的Cookie
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # 如果距上次访问已超过一天.day, 一秒.seconds……
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1

        # 增加访问次数后更新“last_visit_cookie”
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        # 设定“last_visit”cookie
        response.set_cookie('last_visit', last_visit_cookie)

    # 更新或设定“visits”cookie
    response.set_cookie('visits', visits)


# 辅助函数
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


# 更新后的函数定义
def visitor_cookie_handler(request):
    # 获取网站的访问次数
    visits = int(get_server_side_cookie(request, 'visit', '1'))

    # 获取最后访问时间的Cookie
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # 如果距上次访问已超过一天.day, 一秒.seconds……
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1

        # 增加访问次数后更新“last_visit_cookie”
        request.session['last_visit'] = str(datetime.now())
    else:
        # 设定“last_visit”cookie
        request.session['last_visit'] = last_visit_cookie

        # 更新或设定“visits”cookie
    request.session['visits'] = visits
