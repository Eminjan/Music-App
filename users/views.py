from django.contrib import auth
from django.shortcuts import render, redirect
import datetime
from django.core.urlresolvers import reverse
from django_redis import get_redis_connection
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.backends import ModelBackend
# 密码进行加密
from django.contrib.auth.hashers import make_password
# 数据库并集运算
from django.db.models import Q
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
# 发送邮件
from music.models import Singer,Music, Video
from utils.email_send import send_register_email
from .forms import RegisterForm, LoginForm,ModifyPwdForm,UpdateUserProfileForm,UploadAvatarForm, ActiveForm
from .models import UserProfile, EmailVerifyRecord
from operation.models import UserMessage
from operation.models import UserMessage,FavoriteMusic
from utils.mixin import LoginRequiredMixin


# Create your views here.

class IndexView(View):
    """
    首页
    """
    def get(self,request):

        hot_singer = Singer.objects.filter(isHot=True).order_by('-fav_nums')[:5]
        all_music = Music.objects.filter(isHot=True).order_by("-click_nums")[:12]
        new_musics = Music.objects.filter(isNew=True).order_by("-click_nums")[:8]
        return render(request,"index.html",{
            'hot_singer':hot_singer,
            'all_music':all_music,
            'new_musics':new_musics,

        })


class CustomBackend(ModelBackend):
    """
    实现用户名邮箱均可登录
    继承ModelBackend类，因为它有方法authenticate，可点进源码查看
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None

#
class ActiveUserView(View):
    """
    用户激活视图
    """

    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, "login.html", )
        else:
            return render(
                request, "register.html", {
                    "msg": "您的激活链接无效", "active_form": active_form})


class RegisterView(View):
    """
    注册功能的view
    """

    # get方法直接返回页面
    def get(self, request):
        register_form = RegisterForm()
        return render(
            request, 'register.html', {'register_form': register_form}
        )

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 这里注册时前端的name为email
            user_name = request.POST.get("email", "")
            # 用户查重
            if UserProfile.objects.filter(email=user_name):
                return render(
                    request, "register.html", {
                        "register_form": register_form, "msg": "用户已存在！"
                    }
                )
            pass_word = request.POST.get("password", "")

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 默认激活状态为false
            user_profile.is_active = False
            # 加密password进行保存
            user_profile.password = make_password(pass_word)
            user_profile.save()

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册【听音乐】小站!! --系统自动消息"
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, "login.html", {
                "msg":"注册成功,请前往邮箱激活账号"
            })
        else:
            return render(
                request, "register.html", {
                    "register_form": register_form})


class LoginView(View):
    """
    登录视图
    """

    def get(self, request):
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        redirect_url = request.GET.get('next', '')
        return render(request, "login.html", {
            "redirect_url": redirect_url
        })

    def post(self, request):
        # 类实例化需要一个字典参数dict:request.POST就是一个QueryDict所以直接传入
        # POST中的usernamepassword，会对应到form中
        login_form = LoginForm(request.POST)
        # is_valid判断我们字段是否有错执行我们原有逻辑，验证失败跳回login页面
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)
            # if user is not None:
            #     login(request, user)
            #     return redirect(request.GET.get('from', reverse('index')))
            # else:
            #     return render(request, 'login.html', {'msg': '用户名或密码错误'})
            # 如果不是null说明验证成功
            if user is not None:
                # 只有当用户激活时才给登录
                if user.is_active:
                    # login_in 两参数：request, user
                    # 实际是对request写了一部分东西进去，然后在render的时候：
                    # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                    login(request, user)
                    # 跳转到首页 user request会被带回到首页
                    # 增加重定向回原网页。
                    redirect_url = request.POST.get('next', '')
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    # 跳转到首页 user request会被带回到首页
                    return HttpResponseRedirect(reverse("index"))
                # 即用户未激活跳转登录，提示未激活
                else:
                    return render(
                        request, "login.html", {
                            "msg": "用户名未激活! 请前往邮箱进行激活"})
            # 仅当用户真的密码出错时
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
                # 验证不成功跳回登录页面
                # 没有成功说明里面的值是None，并再次跳转回主页面
        else:
            return render(
                request, "login.html", {
                    "login_form": login_form})


class LogoutView(View):
    """
    退出视图
    """

    def get(self, request):
        # django自带的logout
        logout(request)
        # 重定向到首页,
        return HttpResponseRedirect(reverse("index"))


class UserCenterView(LoginRequiredMixin,View):
    """
    用户中心
    """

    def get(self,request):
        user = request.user
        all_message = UserMessage.objects.filter(user=request.user.id)
        # 获取用户的历史音乐浏览记录
        conn= get_redis_connection('default')
        history_key = 'history_%d' % user.id
        # 获取用户最新浏览的5个音乐的id
        music_ids = conn.lrange(history_key, 0, 4)  # [2,3,1]
        # 遍历获取用户浏览的音乐信息
        musics_li = []
        for id in music_ids:
            music = Music.objects.get(id= id)
            musics_li.append(music)


        fav_musics = FavoriteMusic.objects.all().order_by('-id')
        # 用户进入个人中心消息页面，清空未读消息记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 这里指从中取五个出来，每页显示5个
        p = Paginator(all_message, 4)
        messages = p.page(page)
        return render(request, "user_profile.html", {
            "user":user,
            "messages": messages,
            "musics_li":musics_li,
            "fav_musics":fav_musics,
        })


class UpdateUserProfileView(View):
    """
    修改个人资料
    """

    def get(self,request):
        update_form = UpdateUserProfileForm(request.POST)
        return render(request, "update_user_profile.html",{"update_form":update_form})

    def post(self,request):
        update_form = UpdateUserProfileForm(request.POST)
        if update_form.is_valid():
            user_name = request.POST.get("username","")
            # 用户名查重
            if UserProfile.objects.filter(username = user_name):
                return render(request,"update_user_profile.html",{
                    "update_form":update_form,"msg":"用户名已占用"
                })
            email = request.POST.get("email","")
            # 邮箱查重
            if UserProfile.objects.filter(email = email):
                return render(request,"update_user_profile.html",{
                    "update_form":update_form,"msg":"邮箱已存在"
                })
            birthday = request.POST.get("birthday","")
            mobile = request.POST.get("mobile","")
            user = request.user
            user.username = user_name
            user.email = email
            user.birthday = birthday
            user.mobile = mobile
            user.save()
            return render(request,"user_profile.html")
        else:
            return render(request,"update_user_profile.html",{
                "update_form":update_form,"msg":"修改失败"
            })


class UploadAvatarView(View):
    """
    上传修改头像
    """

    def post(self, request):
        # 这时候用户上传的文件就已经被保存到imageform了 ，为modelform添加instance值直接保存
        avatar_form = UploadAvatarForm(
            request.POST, request.FILES, instance=request.user)
        if avatar_form.is_valid():
            avatar_form.save()
            # # 取出cleaned data中的值,一个dict
            avatar = avatar_form.cleaned_data['avatar']
            request.user.avatar = avatar
            request.user.save()
            return render(request,"update_user_profile.html",{

            })
        else:
            return render(request,"update_user_profile.html",{
                "avatar_form":avatar_form,"msg":"上传失败"
            })


class ModifyPwdView(View):
    """
    修改密码
    """

    def get(self, request):
        modify_form = ModifyPwdForm(request.POST)
        return render(request, 'modify_pwd.html', {'modify_form': modify_form})

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'modify_pwd.html', { 'msg': '密码不一致'})
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponseRedirect(reverse("login"))
        else:
            return render(
                request, "modify_pwd.html", {
                    "modify_form": modify_form})


class UserMessageView(View):
    """
    用户消息通知
    """

    def get(self,request):
        all_message = UserMessage.objects.filter(user= request.user.id)
        # 用户进入个人中心消息页面，清空未读消息记录
        all_unread_messages = UserMessage.objects.filter(user = request.user.id,has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 这里指从中取五个出来，每页显示5个
        p = Paginator(all_message, 4)
        messages = p.page(page)
        return render(request, "user_profile.html", {
            "messages": messages,
        })


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
