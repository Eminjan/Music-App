from datetime import datetime

from django.db import models
from users.models import UserProfile
from music.models import Music, Video


# Create your models here.

class MusicComment(models.Model):
    """
    音乐评论
    """
    music = models.ForeignKey(Music, on_delete=models.CASCADE, verbose_name="评论所属的音乐")
    user = models.ForeignKey(UserProfile, max_length=32, verbose_name="评论者")
    content = models.TextField(default='', verbose_name="评论详情")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "音乐评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})对于《{1}》 评论 :'.format(self.name, self.music)


class VideoComment(models.Model):
    """
    视频评论
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="评论所属的视频")
    user = models.ForeignKey(UserProfile, max_length=32, verbose_name="评论者")
    content = models.TextField(default='', verbose_name="评论详情")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})对于《{1}》 评论 :'.format(self.name, self.video)


class FavoriteMusic(models.Model):
    """
    用户收藏音乐
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, verbose_name='音乐')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "音乐收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})收藏了{1} '.format(self.user, self.music)


class FavoriteVideo(models.Model):
    """
    用户收藏视频
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='视频')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "视频收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})收藏了{1} '.format(self.user, self.video)


class UserMessage(models.Model):
    """
    用户消息通知
    """
    user = models.IntegerField(default=0, verbose_name='接受用户')
    message = models.CharField(max_length=200, verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})接受了{1}'.format(self.user, self.message)


class UserMusic(models.Model):
    """
    用户收听的音乐
    """
    music = models.ForeignKey(Music, on_delete=models.CASCADE, verbose_name="音乐")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收听时间")

    class Meta:
        verbose_name = '用户收听音乐'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})收听了{1} '.format(self.user, self.music)
