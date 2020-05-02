from django.urls import path
from .views import register
# from django.conf.urls import url
from . import views
from IYF_K.views import (
	home_page
	)
# from django.conf.urls import patterns,include,url
from django.conf.urls import include,url
from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
# app_name='register_activate'
app_name='user'
urlpatterns = [
	re_path(r'^$',home_page, name='main'),
	re_path(r'^signup/$',views.register, name='register'),
	re_path(r'^activation/',views.activate, name='activation'),
	re_path(r'^signin/$',views.sign_in, name='signin'),
	re_path(r'^logout/$',views.log_out, name='logout'),
	path('counselees/', views.counselees, name = 'counselees')
	]
urlpatterns +=staticfiles_urlpatterns()

