"""Lmusic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.views.static import serve


from users.views import IndexView,RegisterView,LoginView,LogoutView,UserCenterView,ModifyPwdView,UpdateUserProfileView,\
    UploadAvatarView,UserMessageView, ActiveUserView
from music.views import MusicTypeView,NewsView,VideoListView,VideoDetailView,SingerListView,SingerDetailView,\
    MusicTypeDetailView,RecommendView,MusicPlayView,SearchView

from operation.views import MusicCommentView,FavoriteMusicView,VideoCommentView
import xadmin
from Lmusic.settings import MEDIA_ROOT

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/',xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name= "user_active"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^search_result/$',SearchView.as_view(),name='search_result'),
    url('^music_type/$',MusicTypeView.as_view(),name="music_type"),
    url('^news/$',NewsView.as_view(),name="news"),
    url('^video_list/$',VideoListView.as_view(),name="video_list"),
    # url('^video/(?P<video_id>\d+)/$',VideoPlayView.as_view(),name="video_play"),
    url('^video_detail/(?P<video_id>\d+)/$',VideoDetailView.as_view(),name="video_detail"),
    url('^user_center/$',UserCenterView.as_view(),name="user_center"),
    url('^singer_list/$',SingerListView.as_view(),name="singer_list"),
    url('^singer_detail/(?P<singer_id>\d+)/$',SingerDetailView.as_view(),name="singer_detail"),
    url('^modify_pwd/$',ModifyPwdView.as_view(),name="modify_pwd"),
    url('^music_type/(?P<music_type_id>\d+)/$',MusicTypeDetailView.as_view(),name = "music_with_type"),
    # url('^user_fav/$',UserFav.as_view(),name="user_fav"),
    url('^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url('^update_profile/$',UpdateUserProfileView.as_view(),name="update_profile"),
    url('^upload_avatar/$',UploadAvatarView.as_view(),name="upload_avatar"),
    url('^user_message/$',UserMessageView.as_view(),name="user_message"),
    url('^recommend/$',RecommendView.as_view(),name="recommend"),
    # url('^video_comment/$',VideoCommentView.as_view,name="video_comment"),
    url('^music_play/(?P<music_id>\d+)/$',MusicPlayView.as_view(),name="music_play"),
    url('^music_comment/$', MusicCommentView.as_view(), name='music_comment'),
    url('^fav_music/$',FavoriteMusicView.as_view(),name="fav_music"),
    url('^video_comment/$', VideoCommentView.as_view(), name='video_comment'),
    # url('^add_fav/$',AddFavView.as_view(),name="add_fav"),








]

handler404 = 'users.views.page_not_found'

handler500 = 'users.views.page_error'
