"""Rodzynka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path

from Rodzynka import settings
from calendars.views import CalendarDetailView, EventCreateView, CalendarCreateView, CalendarSetUsersView, \
    EventDeleteView, EventUpdateView
from family.views import FamilyMainView, FamilyPickView, IndexView, FamilyCreateView, FamilyInviteView, FamilyJoinView, \
    FamilyAddUserView, FamilyRequestJoinView
from gallery.views import GalleryPickView, GalleryDetailView, GalleryMediaCreateView, GalleryMediaDeleteView, \
    GalleryDeleteView, GalleryCreateView
from users.views import SignupView
from wishlist.views import WishlistView, WishCreateView, WishDeleteView, WishUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^signup/$', SignupView.as_view(), name='signup'),

    re_path(r'^$', IndexView.as_view(), name='index'),

    re_path(r'^family/pick/$', FamilyPickView.as_view(), name='family_pick'),
    re_path(r'^family/create/$', FamilyCreateView.as_view(), name='family_create'),
    re_path(r'^family/requestjoin/$', FamilyRequestJoinView.as_view(), name='family_request_join'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/add/(?P<user_pk>[\d]+)/$',
            FamilyAddUserView.as_view(), name='family_add_user'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/$', FamilyMainView.as_view(), name='family_main'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/invite/$', FamilyInviteView.as_view(), name='family_invite'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/join/$', FamilyJoinView.as_view(), name='family_join'),

    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/gallery/pick/$', GalleryPickView.as_view(), name='gallery_pick'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/gallery/(?P<gallery_pk>[\d]+)/$',
            GalleryDetailView.as_view(), name='gallery_detail'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/gallery/add/$', GalleryCreateView.as_view(), name='gallery_create'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/gallery/delete/(?P<gallery_pk>[\d]+)/$',
            GalleryDeleteView.as_view(), name='gallery_delete'),

    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/gallery/(?P<gallery_pk>[\d]+)/add/$',
            GalleryMediaCreateView.as_view(), name='gallery_media_add'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/gallery/(?P<gallery_pk>[\d]+)/delete/(?P<media_pk>[\d]+)/$',
            GalleryMediaDeleteView.as_view(), name='gallery_media_delete'),

    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/wishlist/$', WishlistView.as_view(), name='wishlist'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/wishlist/add/$', WishCreateView.as_view(), name='wish_create'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/wishlist/delete/(?P<wish_pk>[\d]+)/$', WishDeleteView.as_view(),
            name='wish_delete'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/wishlist/update/(?P<wish_pk>[\d]+)/$', WishUpdateView.as_view(),
            name='wish_update'),

    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/calendar/$', CalendarDetailView.as_view(), name='calendar_detail'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/calendar/(?P<calendar_pk>[\d]+)/$',
            CalendarDetailView.as_view(), name='calendar_detail'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/calendar/(?P<calendar_pk>[\d]+)/(?P<year>[\d]{4})/(?P<month>[\d]+)/$',
            CalendarDetailView.as_view(), name='calendar_detail'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/calendar/create/$',
            CalendarCreateView.as_view(), name='calendar_create'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/calendar/(?P<calendar_pk>[\d]+)/user/add/$',
            CalendarSetUsersView.as_view(), name='calendar_set_users'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/calendar/(?P<calendar_pk>[\d]+)/event/add/(?P<year>[\d]{4})/(?P<month>[\d]+)/(?P<day>[\d]+)/$',
            EventCreateView.as_view(), name='event_create'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/calendar/(?P<calendar_pk>[\d]+)/event/delete/(?P<event_pk>[\d]+)/(?P<year>[\d]{4})/(?P<month>[\d]+)/',
            EventDeleteView.as_view(), name='event_delete'),
    re_path(r'^family/(?P<family_slug>[a-z\d-]+)/calendar/(?P<calendar_pk>[\d]+)/event/update/(?P<event_pk>[\d]+)/(?P<year>[\d]{4})/(?P<month>[\d]+)/',
            EventUpdateView.as_view(), name='event_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
