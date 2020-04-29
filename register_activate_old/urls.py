from django.conf.urls import url
from . import views
from IYF_K.views import (
	home_page
	)
# from django.conf.urls import patterns,include,url
from django.conf.urls import include,url
from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
app_name='register_activate'
urlpatterns = [
	# ex: /register_activate/
	# re_path(r'^$',views.mainpage, name='main'),
	re_path(r'^$',home_page, name='main'),
	# ex: /register_activate/signup/
	re_path(r'^signup/$',views.sign_up, name='signup'),
	# ex: /register_activate/activation/
	re_path(r'^activation/',views.activate, name='activation'),
	# ex: /register_activate/signin/
	re_path(r'^signin/$',views.sign_in, name='signin'),
	# ex: /register_activate/logout/
	re_path(r'^logout/$',views.log_out, name='logout'),

	]
urlpatterns +=staticfiles_urlpatterns()