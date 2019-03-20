from datetime import datetime

from django.db import models

# Create your models here.

class MusicType(models.Model):
    """
    音乐标签
    """
    type_name = models.CharField(max_length=20,verbose_name="音乐类型")

    class Meta:
        verbose_name = "音乐类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name


class Singer(models.Model):
    """
    歌手
    """
    name = models.CharField(max_length=24,verbose_name="歌手名称")
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), default='female', verbose_name='性别',
                              max_length=6)
    desc = models.CharField(max_length=100,verbose_name="歌手简述")
    national = models.CharField(default="中国",max_length=20,verbose_name="国籍")
    isHot = models.BooleanField(default=False,verbose_name="是否热门")
    avatar = models.ImageField(default='',upload_to='singer/%Y/%m',verbose_name="头像",max_length=200)
    fav_nums = models.IntegerField(default=0,verbose_name="收藏数")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "歌手"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Music(models.Model):
    """
    音乐信息
    """
    music_name = models.CharField(max_length=32,verbose_name="音乐名")
    music_type = models.ForeignKey(MusicType,on_delete=models.CASCADE,verbose_name="音乐类型",null=True,blank=True)
    image = models.ImageField(default='',upload_to='music/%Y/%m',verbose_name='封面',max_length=100)
    fav_nums = models.IntegerField(default=0,verbose_name="收藏数")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    comment_nums = models.IntegerField(default=0,verbose_name='评论数')
    singer = models.ForeignKey(Singer,on_delete=models.CASCADE,verbose_name="作者",null=True,blank=True)
    music_time = models.CharField(default='',max_length=10,verbose_name="时长")
    isHot = models.BooleanField(default=False, verbose_name="是否热门")
    isNew = models.BooleanField(default=False,verbose_name="是否新歌")
    music_file = models.FileField(default='',upload_to="song/%Y/%m",verbose_name="音乐文件")
    music_language = models.CharField(default="中文",max_length=20,verbose_name="语种")
    release_time = models.DateTimeField(default=datetime.now,verbose_name="发布时间")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "音乐"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.music_name


class Video(models.Model):
    """
    视频Model
    """
    video_name = models.CharField(max_length=32,verbose_name="视频名")
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, verbose_name="作者", null=True, blank=True)
    image = models.ImageField(default='',upload_to='video/%Y/%m',max_length=100,verbose_name="视频封面")
    video_file = models.FileField(upload_to='video/src/%Y/%m',verbose_name="视频文件")
    desc = models.CharField(max_length=300, verbose_name='视频描述描述')
    fav_nums = models.IntegerField(default=0,verbose_name="收藏数")
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    video_time = models.CharField(default='',max_length=10, verbose_name="时长")
    isRecommend = models.BooleanField(default=False,verbose_name="是否要推荐")
    comment_nums = models.IntegerField(default=0,verbose_name="评论数")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.video_name


class News(models.Model):
    """
    新闻动态model
    """
    title = models.CharField(max_length=50,verbose_name="新闻标题")
    content = models.CharField(max_length=200,verbose_name="内容")
    singer = models.ForeignKey(Singer,on_delete=models.CASCADE,verbose_name="关联的歌手")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "新闻"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

