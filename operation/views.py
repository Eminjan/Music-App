#!/usr/bin/env
# -*-coding:utf-8-*-
# @Author  : E🚀M

from django.shortcuts import render, render_to_response
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from music.models import Music, Video
from .models import MusicComment, FavoriteMusic, VideoComment
from .forms import MusicCommentForm, VideoCommentForm


class MusicCommentView(View):
    """
    音乐评论
    """

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')
        add_form = MusicCommentForm(request.POST)
        if add_form.is_valid():
            content = request.POST.get("content", "")
            music_id = request.POST.get("music_id", "")
            comment = MusicComment(
                user=request.user,
                content=content,
                music_id=music_id)
            comment.save()
            music = Music.objects.get(id=music_id)
            music.comment_nums += 1
            music.save()
            return HttpResponseRedirect(
                reverse("music_play", args=(music_id,)))
        else:
            return HttpResponse('重新评论')


class VideoCommentView(View):
    """
    视频评论
    """

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')
        add_form = VideoCommentForm(request.POST)
        if add_form.is_valid():
            content = request.POST.get("content", "")
            video_id = request.POST.get("video_id", "")
            comment = VideoComment(
                user=request.user,
                content=content,
                video_id=video_id)
            comment.save()
            video = Video.objects.get(id=video_id)
            video.comment_nums += 1
            video.save()
            return HttpResponseRedirect(
                reverse("video_detail", args=(video_id,)))
        else:
            return HttpResponse('重新评论')


class FavoriteMusicView(View):
    """
    音乐收藏View
    """

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')

        music_id = request.POST.get("music_id", "")
        fav_music = FavoriteMusic(user=request.user, music_id=music_id)
        fav_music.save()

        return HttpResponseRedirect(reverse("music_play", args=(music_id,)), {
            "fav_music": fav_music,

        })

        # class AddFavView(View):
        #     """
        #     用户收藏与取消功能
        #     """
        #
        #     def post(self, request):
        #         id = request.POST.get("music_id", "")
        #
        #         if not request.user.is_authenticated:
        #             # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
        #             return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        #         exit_records = FavoriteMusic.objects.filter(user = request.user,music_id=int(id))
        #         if exit_records:
        #             exit_records.delete()
        #             music = Music.objects.get(id = int(id))
        #             music.fav_nums-=1
        #             return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        #         else:
        #             fav_music = FavoriteMusic
        #             if int(id)>0:
        #                 fav_music.music_id = int(id)
        #                 fav_music.save()
        #
        #                 return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
        #             else:
        # return HttpResponse('{"status":"fail", "msg":"收藏出错"}',
        # content_type='application/json')
