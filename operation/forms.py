#!/usr/bin/env
# -*-coding:utf-8-*-
# @Author  : E🚀M

from django import forms


class MusicCommentForm(forms.Form):
    """
    音乐评论表单
    """
    content = forms.CharField(required=True)


class VideoCommentForm(forms.Form):
    """
    视频评论表单
    """
    content = forms.CharField(required=True)

