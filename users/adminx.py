#!/usr/bin/env
# -*-coding:utf-8-*-
# @Author  : E🚀M

import xadmin
from xadmin import views
from . models import UserProfile, EmailVerifyRecord


class BaseSetting(object):
    """X admin的全局配置设置"""
    # 主题功能开启
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    """xadmin 全局配置参数信息设置"""
    site_title = "听·音乐管理后台"
    site_footer = "听·音乐"
    # 收起菜单
    # menu_style = "accordion"


# class UserProfileAdmin(object):
#     """
#     注册用户信息
#     """
#     list_display = ['id','username','nick_name','gender','mobile']
#     search_fields = ['username','mobile']
#     ordering = ['-id']
#     list_editable = ['mobile','gender']
#     model_icon = 'fa fa-users'


class EmailVerifyRecordAdmin(object):
    """
    注册验证码信息
    """
    list_display = ['id', 'code', 'email', 'send_type', 'send_time']
    ordering = ['-id']
    list_editable = ['code', 'send_type']
    model_icon = 'fa fa-code'


# 将Xadmin全局管理器与我们的view绑定注册。
xadmin.site.register(views.BaseAdminView, BaseSetting)
# 将头部与脚部信息进行注册:
xadmin.site.register(views.CommAdminView, GlobalSettings)
# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
