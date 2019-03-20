#!/usr/bin/env
# -*-coding:utf-8-*-
# @Author  : E🚀M

import xadmin
from .models import UserMusic,FavoriteMusic,UserMessage,MusicComment,VideoComment,FavoriteVideo

class UserMusicAdmin(object):
    """
    注册用户收听的音乐到后台
    """
    list_display = ['id','music','user',]
    search_fields = ['music','user',]
    list_filter = ['music','user',]
    ordering = ['-id']
    model_icon = 'fa fa-play'


class FavoriteMusicAdmin(object):
    """
    注册音乐收藏到后台
    """
    list_display = ['id','user','music','add_time']
    ordering = ['-id']
    list_filter = ['add_time']
    model_icon = 'fa fa-heart'


class UserMessageAdmin(object):
    """
    注册用户消息到后台
    """
    list_display = ['id','user','has_read']
    list_filter = ['add_time','has_read']
    ordering = ['-id']
    model_icon = 'fa fa-bell'


class MusicCommentAdmin(object):
    """
    音乐评论注册到后台
    """
    list_display = ['id','music','user','add_time']
    search_fields = ['music']
    list_filter = ['user','add_time']
    ordering = ['-id']
    model_icon = 'fa fa-comment'


class VideoCommentAdmin(object):
    """
    video评论注册到后台
    """
    list_display = ['id','video','user','add_time']
    search_fields = ['video']
    list_filter = ['user','add_time']
    ordering = ['-id']
    model_icon = 'fa fa-comment'


xadmin.site.register(UserMusic,UserMusicAdmin)
xadmin.site.register(FavoriteMusic,FavoriteMusicAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(MusicComment,MusicCommentAdmin)
xadmin.site.register(VideoComment,VideoCommentAdmin)