from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'clubinfo'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^profiles/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name="profile"),
    url(r'^delete/(?P<ann_id>[0-9]+)/$', views.delete, name='delete'),
    url(r'^undo_announcement/$', views.undo_announcement, name='undo_announcement'),
    url(r'^announcement/(?P<pk>[0-9]+)/$', views.AnnouncementView.as_view(), name="announcement"),
    url(r'^contests/$', views.contest_home, name='contest_home'),
    url(r'^contest_details/(?P<pk>[0-9]+)/$', views.contest_details, name='contest_details'),
    url(r'^modify_contest/(?P<pk>[0-9]+)/$', views.modify_contest, name='modify_contest'),
    url(r'^mod_contest_info/(?P<pk>[0-9]+)/$', views.mod_contest_info, name='mod_contest_info'),
    url(r'^mod_contest_del_user/(?P<score_pk>[0-9]+)/$', views.mod_contest_del_user, name='mod_contest_del_user'),
    url(r'^mod_contest_add_user/(?P<user_pk>[0-9]+)/(?P<contest_pk>[0-9]+)/$', views.mod_contest_add_user, name='mod_contest_add_user'),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # need this for static files i guess