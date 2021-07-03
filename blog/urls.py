from django.conf.urls import url, include
from django.contrib import admin
from blog.views import CreateBlog, UserLogin, DisplayBlog, DeleteBlog, UpdateBlog,\
CommentOnBlog, LikeBlog, ReportBlog, UserSignUp

urlpatterns = [
    url(r'^login/$', UserLogin.as_view(), name="UserLogin"),
    url(r'^signup/$', UserSignUp.as_view(), name="UserSignUp"),
    url(r'^create/$', CreateBlog.as_view(), name="BlogAPIView"),
    url(r'^details/(?P<id>all|\d+)/$', DisplayBlog.as_view(), name="DisplayBlog"),
    url(r'^delete/(?P<id>\d+)/$', DeleteBlog.as_view(), name="DeleteBlog"),
    url(r'^update/$', UpdateBlog.as_view(), name="UpdateBlog"),
    url(r'^comment/(?P<blog_id>\d+)/$', CommentOnBlog.as_view(), name="CommentOnBlog"),
    url(r'^like/(?P<blog_id>\d+)/$', LikeBlog.as_view(), name="LikeBlog"),
    url(r'^report/(?P<blog_id>\d+)/$', ReportBlog.as_view(), name="ReportBlog"),
]
