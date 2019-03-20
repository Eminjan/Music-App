#!/usr/bin/env
# -*-coding:utf-8-*-
# @Author  : E🚀M

import xadmin
from .models import MusicType,Singer,Music,Video,News

class MusicTypeAdmin(object):
    list_display =['id','type_name']
    search_fields = ['type_name']
    ordering = ['-id']
    model_icon = 'fa fa-tags'
    list_display_links = ['id','type_name']


class SingerAdmin(object):
    list_display = ['id','name','national','isHot','fav_nums']
    search_fields = ['name','national']
    list_filter = ['name','isHot','fav_nums']
    list_editable = ['isHot','fav_nums']
    ordering = ['-id']
    model_icon = 'fa fa-user'
    list_display_links = ['id','name','national']


class MusicAdmin(object):
    list_display = ['id','music_name','music_type','music_language','fav_nums','click_nums','release_time','isHot','isNew']
    search_fields = ['music_name','music_type']
    list_filter = ['music_name','music_language','music_type','isHot']
    list_editable = ['isHot','isNew','fav_nums','click_nums']
    ordering = ['-id']
    model_icon = 'fa fa-music'
    list_display_links = ['id','music_name','music_type','music_language']



class VideoAdmin(object):
    list_display = ['id','video_name','fav_nums','click_nums','comment_nums']
    list_filter = ['video_name','click_nums']
    search_fields = ['video_name']
    list_editable = ['click_nums,fav_nums']
    ordering = ['-id']
    model_icon = 'fa fa-film'
    list_display_links = ['id','video_name']


class NewsAdmin(object):
    list_display = ['id','title','singer','add_time']
    list_filter = ['singer','add_time']
    list_editable = ['singer','title','add_time']
    ordering = ['-id']
    model_icon = 'fa fa-file-text'
    list_display_links = ['id','title','singer']


xadmin.site.register(MusicType,MusicTypeAdmin)
xadmin.site.register(Singer,SingerAdmin)
xadmin.site.register(Music,MusicAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(News,NewsAdmin)
