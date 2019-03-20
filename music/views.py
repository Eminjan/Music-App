import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponse
from django_redis import get_redis_connection

from music import models
from .models import MusicType, Singer, Music, Video, News
from operation.models import MusicComment, VideoComment
from utils.mixin import LoginRequiredMixin


# Create your views here.

class SearchView(View):
    """
    搜索视图
    """

    def get(self, request):
        search_keywords = request.GET.get('keywords', '')

        se_musics = Music.objects.filter(music_name__icontains=search_keywords)
        counts = se_musics.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(se_musics, 8, request=request)
        se_musics = p.page(page)
        return render(request, "search.html", {
            "se_musics": se_musics,
            "search_keywords": search_keywords,
        })


class MusicTypeView(View):
    """
    音乐分类视图
    """

    def get(self, request):
        all_music = Music.objects.get_queryset().order_by('id')
        music_types = MusicType.objects.all()
        # 生成paginator对象,定义每页显示10条记录
        paginator = Paginator(all_music, 12)
        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)
        # 把当前的页码数转换成整数类型
        currentPage = int(page)
        try:
            # 获取当前页码的记录
            all_music = paginator.page(page)
        except PageNotAnInteger:
            # 如果用户输入的页码不是整数时,显示第1页的内容
            all_music = paginator.page(1)
        except EmptyPage:
            # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
            all_music = paginator.page(paginator.num_pages)

        return render(request, "music_type.html", {
            "all_music": all_music,
            "music_types": music_types,
        })


class NewsView(View):
    """
    新闻动态视图
    """

    def get(self, request):
        all_news = News.objects.all().order_by('-id')
        counts = all_news.count()
        return render(request, 'news.html', {
            "all_news": all_news,
            "counts":counts,
        })


class VideoListView(View):
    """
    video视图
    """

    def get(self, request):
        recommend_video = Video.objects.filter(isRecommend=True).order_by('-click_nums')[:3]
        all_video = Video.objects.get_queryset().order_by('id')
        # 生成paginator对象,定义每页显示10条记录
        paginator = Paginator(all_video, 12)
        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)
        # 把当前的页码数转换成整数类型
        currentPage = int(page)
        try:
            # 获取当前页码的记录
            all_video = paginator.page(page)
        except PageNotAnInteger:
            # 如果用户输入的页码不是整数时,显示第1页的内容
            all_video = paginator.page(1)
        except EmptyPage:
            # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
            all_video = paginator.page(paginator.num_pages)

        return render(request, "video_list.html", {
            "recommend_video": recommend_video,
            "all_video": all_video,
        })


class VideoDetailView(LoginRequiredMixin,View):
    """
    video_play视图
    """

    def get(self, request, video_id, ):
        video = Video.objects.get(id=int(video_id))
        recommend_video = Video.objects.get_queryset().order_by('-click_nums')[:7]
        video.click_nums += 1
        video.save()
        comments = VideoComment.objects.filter(video_id=video_id).order_by('-add_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(comments, 8, request=request)
        comments = p.page(page)

        video_singer = video.singer_id
        # user = request.user
        # if user.is_authenticated():
        #     # 添加用户历史记录
        #     conn = get_redis_connection('default')
        #     history_key = 'history_%d' % user.id
        #     # 移除列表中的video_id
        #     conn.lrem(history_key, 0, video_id)
        #     # 把video_id 插入到列表的左侧
        #     conn.lpush(history_key, video_id)
        #     # 只保存用户的最新的5条记录
        #     conn.ltrim(history_key, 0, 4)
        return render(request, "video_detail.html", {
            "video": video,
            "recommend_video": recommend_video,
            "video_singer": video_singer,
            "comments": comments,
        })


class SingerListView(View):
    """
    歌手列表
    """

    def get(self, request):
        hot_singer = Singer.objects.filter(isHot=True).order_by('-fav_nums')[:5]
        return render(request, "index.html", {
            "hot_singer": hot_singer
        })


class SingerDetailView(LoginRequiredMixin,View):
    """
    歌手详情
    """

    def get(self, request, singer_id, ):
        singer = Singer.objects.get(id=int(singer_id))
        singer_name = get_object_or_404(Singer, pk=singer_id)
        singer_musics = Music.objects.filter(singer=singer_name)
        singer_videos = Video.objects.filter(singer=singer_name)
        singer_music_count = singer_musics.count()
        singer_video_count = singer_videos.count()
        return render(request, "singer_detail.html", {
            "singer": singer,
            "singer_musics": singer_musics,
            "singer_videos": singer_videos,
            "singer_music_count": singer_music_count,
            "singer_video_count": singer_video_count,
        })


class MusicTypeDetailView(View):
    """
    音乐类型包含的音乐
    """

    def get(self, request, music_type_id):
        music_types = MusicType.objects.all()
        music_type = MusicType.objects.get(id=int(music_type_id))
        music_type_name = get_object_or_404(MusicType, pk=music_type_id)
        music_type_musics = Music.objects.filter(music_type=music_type_name).order_by('music_type_id')
        # 生成paginator对象,定义每页显示10条记录
        paginator = Paginator(music_type_musics, 12)
        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)
        # 把当前的页码数转换成整数类型
        currentPage = int(page)
        try:
            # 获取当前页码的记录
            music_type_musics = paginator.page(page)
        except PageNotAnInteger:
            # 如果用户输入的页码不是整数时,显示第1页的内容
            music_type_musics = paginator.page(1)
        except EmptyPage:
            # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
            music_type_musics = paginator.page(paginator.num_pages)
        return render(request, "music_with_type.html", {
            "music_type": music_type,
            "music_type_musics": music_type_musics,
            "music_types": music_types,
        })


class RecommendView(LoginRequiredMixin,View):
    """
    随机推荐
    """

    def get(self, request):
        random_index = random.randint(0, Singer.objects.count() - 1)
        random_singer = Singer.objects.all()[random_index]
        singer_id = random_singer.id
        all_music = Music.objects.filter(singer=random_singer)[:10]
        random_music = Music.objects.all().order_by('?')[:12]
        return render(request, "recommend.html", {
            "random_singer": random_singer,
            "all_music": all_music,
            "random_music": random_music,
            "singer_id": singer_id,
        })


class MusicPlayView(View):
    """
    音乐播放视图
    """

    def get(self, request, music_id):
        music = Music.objects.get(id=int(music_id))
        # 音乐增加点击数
        music.click_nums += 1
        music.save()
        comments = MusicComment.objects.filter(music_id=music_id).order_by('-add_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(comments, 2, request=request)
        comments = p.page(page)
        user = request.user
        if user.is_authenticated():
            # 添加用户历史记录
            conn = get_redis_connection('default')
            history_key = 'history_%d' % user.id
            # 移除列表中的music_id
            conn.lrem(history_key, 0, music_id)
            # 把music_id 插入到列表的左侧
            conn.lpush(history_key, music_id)
            # 只保存用户的最新的5条记录
            conn.ltrim(history_key, 0, 4)
        return render(request, "music_play.html", {
            'music': music,
            'comments': comments,
        })


class SearchView(View):
    """
    搜索视图
    """

    def get(self, request):
        search_keywords = request.GET.get('keywords', '')
        videos = Video.objects.all()
        musics = Music.objects.all()
        if search_keywords:
            musics = Music.objects.filter(music_name__icontains=search_keywords)
            videos = Video.objects.filter(video_name__icontains=search_keywords)
        elif not search_keywords:
            return HttpResponse("请输入输入关键词")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(musics, 10, request=request)
        musics = p.page(page)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(videos, 10, request=request)
        videos = p.page(page)
        return render(request, 'search.html', {"musics": musics, "search_keywords": search_keywords,
                                               "videos": videos,
                                               })
